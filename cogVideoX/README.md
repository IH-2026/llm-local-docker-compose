# CogVideoX Local

A reusable Python library and command-line interface for loading CogVideoX
pipelines and generating videos. The model is selected with `MODEL_ID`; downloaded
files are reused from the Hugging Face cache.

## Requirements

- Python 3.10 or newer
- NVIDIA GPU and a compatible CUDA environment for practical video generation
- Pipenv

The Pipfile selects PyTorch wheels for CUDA 12.4. For other CUDA, CPU-only, or
platform configurations, install the matching PyTorch build for your system
before installing the project dependencies.

## Development setup

```sh
pipenv install --dev
pipenv run pip install -e .
```

The project version is `1.0.0`. Build both distribution formats with `make build`.

## Library usage

```python
from cogvideox import CogVideoXGenerator, GenerationConfig

generator = CogVideoXGenerator(
    GenerationConfig(
        model_id="THUDM/CogVideoX-2b",
        output_dir="output",
    )
)
prompt_file = "prompts/default.txt"
video_path = generator.generate_video(prompt_file)
print(video_path)
```

`generate_video` accepts a path to a UTF-8 text file, not the prompt text itself.
It reads the file contents and raises a `PromptFileError` if the file is
missing, unreadable, invalid-UTF-8, or empty.

`MODEL_ID` can be set to any compatible model identifier available to the
installed Diffusers `CogVideoXPipeline`, for example:

- `THUDM/CogVideoX-2b`
- `THUDM/CogVideoX-5b`
- `THUDM/CogVideoX1.5-5B`
- `THUDM/CogVideoX1.5-5B-I2V`

Pipeline support varies by model architecture. Image-to-video checkpoints may
require a different Diffusers pipeline class than the text-to-video class
currently used by this library.

## Command line

```sh
MODEL_ID=THUDM/CogVideoX-2b pipenv run cogvideox \
  --prompt-file prompts/default.txt
```

Prompts are UTF-8 text files stored in `prompts/`. The CLI defaults to
`prompts/default.txt`; choose another file path with `--prompt-file` or set
`PROMPT_FILE`. The argument/environment variable is the file path, not the
prompt text. With Docker Compose, files in this folder are mounted read-only at
`/workspace/prompts`, so `PROMPT_FILE` must use a container path:

```sh
PROMPT_FILE=/workspace/prompts/my-prompt.txt \
  docker compose -f docker-compose.yaml up --build
```

For a single run without changing the Compose default:

```sh
docker compose -f docker-compose.yaml run --rm cogvideo \
  python3 -u -m cogvideox --prompt-file /workspace/prompts/my-prompt.txt
```

To download/load the model without generating a video:

```sh
MODEL_ID=THUDM/CogVideoX-2b pipenv run cogvideox --preload-only
```

Use `--help` to see command-line options. Models are cached using Hugging Face's
normal cache configuration (`HF_HOME` and related environment variables).

Operational failures are written to stderr with a non-zero process status
(model loading/generation failures use status `1`; argparse usage errors use `2`).
Ctrl-C exits with status `130`. On Docker stop, the CLI logs the SIGTERM and exits
with status `143`; Compose allows up to 30 seconds for shutdown before forcing
termination. Unexpected programming errors retain their traceback and also exit
non-zero.

The Compose service loads the model once in the application process and logs
generation start and periodic denoising-step progress while inference runs.

## Quality checks

```sh
make test
make lint
make build
```
