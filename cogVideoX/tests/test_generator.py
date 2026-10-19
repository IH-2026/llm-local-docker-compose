import logging
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import torch

from cogvideox import CogVideoXGenerator, GenerationConfig
from cogvideox import generator as generator_module
from cogvideox.exceptions import ModelLoadError, PromptFileError


def test_model_is_loaded_once() -> None:
    pipeline = Mock()
    factory = Mock(return_value=pipeline)
    generator = CogVideoXGenerator(
        GenerationConfig(model_id="example/model"),
        pipeline_factory=factory,
    )

    assert generator.load_model() is pipeline
    assert generator.load_model() is pipeline
    factory.assert_called_once_with("example/model", torch_dtype=torch.float16)


def test_model_load_error_includes_model_and_chains_cause() -> None:
    cause = OSError("network unavailable")
    factory = Mock(side_effect=cause)
    generator = CogVideoXGenerator(
        GenerationConfig(model_id="example/model"),
        pipeline_factory=factory,
    )

    with pytest.raises(ModelLoadError, match="example/model") as error:
        generator.load_model()

    assert error.value.__cause__ is cause


def test_generate_video_logs_inference_progress(monkeypatch, caplog, tmp_path) -> None:
    caplog.set_level(logging.INFO)
    pipeline = Mock()
    pipeline.return_value = SimpleNamespace(frames=[["frame"]])
    factory = Mock(return_value=pipeline)
    export = Mock()
    monkeypatch.setattr(generator_module.torch.cuda, "is_available", lambda: False)
    monkeypatch.setattr(generator_module, "export_to_video", export)

    generator = CogVideoXGenerator(
        GenerationConfig(
            model_id="example/model",
            output_dir=tmp_path,
            num_inference_steps=5,
        ),
        pipeline_factory=factory,
    )

    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("A test prompt", encoding="utf-8")

    destination = generator.generate_video(prompt_file)
    callback = pipeline.call_args.kwargs["callback_on_step_end"]
    callback(pipeline, 0, None, {})

    assert destination == tmp_path / "output.mp4"
    assert "Generating video (5 steps" in caplog.text
    assert "Generation progress: 1/5 steps (20%)." in caplog.text
    export.assert_called_once()
    assert pipeline.call_args.kwargs["prompt"] == "A test prompt"


def test_generate_video_rejects_missing_prompt_file(tmp_path) -> None:
    generator = CogVideoXGenerator(
        GenerationConfig(model_id="example/model"),
        pipeline_factory=Mock(),
    )

    with pytest.raises(PromptFileError, match="Could not read"):
        generator.generate_video(tmp_path / "missing.txt")

    generator._pipeline_factory.assert_not_called()


def test_generate_video_rejects_empty_prompt_file(tmp_path) -> None:
    prompt_file = tmp_path / "empty.txt"
    prompt_file.write_text(" \n", encoding="utf-8")
    generator = CogVideoXGenerator(
        GenerationConfig(model_id="example/model"),
        pipeline_factory=Mock(),
    )

    with pytest.raises(PromptFileError, match="is empty"):
        generator.generate_video(prompt_file)

    generator._pipeline_factory.assert_not_called()
