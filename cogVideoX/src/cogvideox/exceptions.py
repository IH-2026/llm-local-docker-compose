"""Exceptions raised by CogVideoX Local."""


class CogVideoXError(Exception):
    """Base class for expected CogVideoX Local operational errors."""


class ModelLoadError(CogVideoXError):
    """Raised when a configured model cannot be loaded."""


class PromptFileError(CogVideoXError):
    """Raised when the prompt file cannot be read or contains no prompt."""


class VideoGenerationError(CogVideoXError):
    """Raised when video generation or output encoding fails."""
