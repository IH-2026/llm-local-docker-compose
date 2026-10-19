from unittest.mock import Mock

from cogvideox import cli
from cogvideox.exceptions import ModelLoadError


def test_main_returns_success_after_preloading(monkeypatch) -> None:
    generator = Mock()
    monkeypatch.setattr(cli, "CogVideoXGenerator", Mock(return_value=generator))

    status = cli.main(["--preload-only", "--model-id", "example/model"])

    assert status == 0
    generator.load_model.assert_called_once_with()
    generator.generate_video.assert_not_called()


def test_main_passes_prompt_file_path_to_generator(monkeypatch, tmp_path) -> None:
    generator = Mock()
    monkeypatch.setattr(cli, "CogVideoXGenerator", Mock(return_value=generator))
    prompt_file = tmp_path / "my-prompt.txt"

    status = cli.main(["--prompt-file", str(prompt_file)])

    assert status == 0
    generator.generate_video.assert_called_once_with(prompt_file)


def test_main_reports_expected_operational_error(monkeypatch, caplog) -> None:
    generator = Mock()
    generator.load_model.side_effect = ModelLoadError("model download failed")
    monkeypatch.setattr(cli, "CogVideoXGenerator", Mock(return_value=generator))

    status = cli.main(["--preload-only"])

    assert status == 1
    assert "ERROR: model download failed" in caplog.text


def test_main_returns_interrupt_status(monkeypatch, caplog) -> None:
    generator = Mock()
    generator.load_model.side_effect = KeyboardInterrupt
    monkeypatch.setattr(cli, "CogVideoXGenerator", Mock(return_value=generator))

    status = cli.main(["--preload-only"])

    assert status == 130
    assert "Interrupted; shutting down." in caplog.text
