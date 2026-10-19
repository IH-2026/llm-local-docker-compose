"""Public API for the CogVideoX video generation library."""

from cogvideox.config import GenerationConfig
from cogvideox.generator import CogVideoXGenerator

__version__ = "1.0.0"

__all__ = ["CogVideoXGenerator", "GenerationConfig", "__version__"]
