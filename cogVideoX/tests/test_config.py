from pathlib import Path

import pytest

from cogvideox.config import GenerationConfig


def test_from_env_uses_model_and_output_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MODEL_ID", "THUDM/CogVideoX-5b")
    monkeypatch.setenv("OUTPUT_DIR", "/tmp/videos")

    config = GenerationConfig.from_env()

    assert config.model_id == "THUDM/CogVideoX-5b"
    assert config.output_dir == Path("/tmp/videos")


def test_config_converts_output_directory_to_path() -> None:
    config = GenerationConfig(output_dir="videos")

    assert config.output_dir == Path("videos")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model_id", " "),
        ("num_inference_steps", 0),
        ("num_frames", 0),
        ("fps", 0),
    ],
)
def test_config_rejects_invalid_values(field: str, value: object) -> None:
    with pytest.raises(ValueError):
        GenerationConfig(**{field: value})
