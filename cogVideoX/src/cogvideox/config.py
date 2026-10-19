"""Configuration for CogVideoX model loading and generation."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class GenerationConfig:
    """Options for loading a model and generating one video."""

    model_id: str = "THUDM/CogVideoX-2b"
    output_dir: Path = Path("output")
    num_inference_steps: int = 50
    num_frames: int = 49
    guidance_scale: float = 6.0
    fps: int = 8
    seed: int = 42

    def __post_init__(self) -> None:
        if not self.model_id.strip():
            raise ValueError("model_id must not be empty")
        object.__setattr__(self, "output_dir", Path(self.output_dir))
        if self.num_inference_steps <= 0:
            raise ValueError("num_inference_steps must be greater than zero")
        if self.num_frames <= 0:
            raise ValueError("num_frames must be greater than zero")
        if self.fps <= 0:
            raise ValueError("fps must be greater than zero")

    @classmethod
    def from_env(cls) -> "GenerationConfig":
        """Create configuration using the standard environment variables."""
        return cls(
            model_id=os.environ.get("MODEL_ID", "THUDM/CogVideoX-2b"),
            output_dir=Path(os.environ.get("OUTPUT_DIR", "output")),
        )
