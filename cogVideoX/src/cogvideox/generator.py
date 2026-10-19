"""Model loading and video-generation service."""

import logging
from pathlib import Path
from typing import Any, Callable

import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video

from cogvideox.config import GenerationConfig
from cogvideox.exceptions import ModelLoadError, PromptFileError, VideoGenerationError

PipelineFactory = Callable[..., Any]
LOGGER = logging.getLogger(__name__)


class CogVideoXGenerator:
    """Load a CogVideoX pipeline and use it to generate videos."""

    def __init__(
        self,
        config: GenerationConfig | None = None,
        pipeline_factory: PipelineFactory = CogVideoXPipeline.from_pretrained,
    ) -> None:
        self.config = config or GenerationConfig.from_env()
        self._pipeline_factory = pipeline_factory
        self._pipeline: Any | None = None

    def load_model(self) -> Any:
        """Load the configured model once, using the Hugging Face cache."""
        if self._pipeline is None:
            try:
                LOGGER.info("Loading model: %s", self.config.model_id)
                self._pipeline = self._pipeline_factory(
                    self.config.model_id,
                    torch_dtype=torch.float16,
                )
                LOGGER.info("MODEL LOADED")
            except Exception as error:
                raise ModelLoadError(
                    f"Could not load model '{self.config.model_id}': {error}"
                ) from error
        return self._pipeline

    def generate_video(
        self,
        prompt_file: str | Path,
        output_path: str | Path | None = None,
    ) -> Path:
        """Generate a video using prompt text read from a UTF-8 file."""
        prompt_path = Path(prompt_file)
        try:
            prompt = prompt_path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as error:
            raise PromptFileError(
                f"Could not read prompt file '{prompt_path}': {error}"
            ) from error
        if not prompt:
            raise PromptFileError(f"Prompt file '{prompt_path}' is empty.")

        destination = Path(output_path) if output_path else (
            self.config.output_dir / "output.mp4"
        )
        pipeline = self.load_model()
        try:
            use_cuda = torch.cuda.is_available()
            device = "cuda" if use_cuda else "cpu"

            LOGGER.info("Preparing generation on %s.", device)
            if use_cuda:
                pipeline.enable_sequential_cpu_offload()
            else:
                pipeline.to(device)

            pipeline.vae.enable_slicing()
            pipeline.vae.enable_tiling()

            generator = torch.Generator(device=device).manual_seed(self.config.seed)
            LOGGER.info(
                "Generating video (%d steps, %d frames).",
                self.config.num_inference_steps,
                self.config.num_frames,
            )

            def log_progress(
                _pipeline: Any,
                step_index: int,
                _timestep: Any,
                callback_kwargs: dict[str, Any],
            ) -> dict[str, Any]:
                completed_steps = step_index + 1
                percentage = completed_steps / self.config.num_inference_steps * 100
                LOGGER.info(
                    "Generation progress: %d/%d steps (%.0f%%).",
                    completed_steps,
                    self.config.num_inference_steps,
                    percentage,
                )
                return callback_kwargs

            result = pipeline(
                prompt=prompt,
                num_videos_per_prompt=1,
                num_inference_steps=self.config.num_inference_steps,
                num_frames=self.config.num_frames,
                guidance_scale=self.config.guidance_scale,
                generator=generator,
                callback_on_step_end=log_progress,
            )

            LOGGER.info("Encoding video to %s.", destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            export_to_video(result.frames[0], str(destination), fps=self.config.fps)
        except Exception as error:
            raise VideoGenerationError(
                f"Could not generate video at '{destination}': {error}"
            ) from error
        return destination
