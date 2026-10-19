"""Command-line interface for CogVideoX Local."""

import argparse
import logging
import os
import signal
from collections.abc import Sequence
from pathlib import Path

import torch

from cogvideox import __version__
from cogvideox.config import GenerationConfig
from cogvideox.exceptions import CogVideoXError
from cogvideox.generator import CogVideoXGenerator

LOGGER = logging.getLogger(__name__)
DEFAULT_PROMPT_FILE = Path(
    os.environ.get("PROMPT_FILE", "prompts/default.txt")
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cogvideox",
        description="Load a CogVideoX model and generate a video.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=DEFAULT_PROMPT_FILE,
        help=(
            "UTF-8 text file containing the video prompt "
            f"(default: {DEFAULT_PROMPT_FILE})."
        ),
    )
    parser.add_argument(
        "--model-id",
        help="Hugging Face model ID (defaults to MODEL_ID or CogVideoX-2b).",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for generated videos (defaults to OUTPUT_DIR or output).",
    )
    parser.add_argument(
        "--preload-only",
        action="store_true",
        help="Load/download the selected model without generating a video.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def _handle_termination(signum: int, _frame: object) -> None:
    LOGGER.warning("Received %s; shutting down.", signal.Signals(signum).name)
    raise SystemExit(128 + signum)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process status suitable for Docker."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    signal.signal(signal.SIGTERM, _handle_termination)
    args = build_parser().parse_args(argv)

    try:
        config = GenerationConfig.from_env()
        if args.model_id:
            config = GenerationConfig(
                model_id=args.model_id,
                output_dir=config.output_dir,
            )
        if args.output_dir:
            config = GenerationConfig(
                model_id=config.model_id,
                output_dir=args.output_dir,
            )

        generator = CogVideoXGenerator(config)
        LOGGER.info("CUDA available: %s", torch.cuda.is_available())

        if args.preload_only:
            generator.load_model()
        else:
            LOGGER.info("Reading prompt from %s", args.prompt_file)
            video_path = generator.generate_video(args.prompt_file)
            LOGGER.info("Video saved to %s", video_path)
        return 0
    except (CogVideoXError, ValueError) as error:
        LOGGER.error("%s", error)
        return 1
    except KeyboardInterrupt:
        LOGGER.warning("Interrupted; shutting down.")
        return 130
