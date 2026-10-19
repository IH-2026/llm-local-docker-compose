---
name: cogvideox-local
description: "Use when building, running, or troubleshooting this repository's CogVideoX Docker service or Python library, including MODEL_ID selection, video-generation progress, GPU use, and container logs."
---

# CogVideoX Local Generator

Use this skill for the finite video-generation job and Python library in
`cogVideoX/`. Read [`cogVideoX/README.md`](../../../cogVideoX/README.md),
[`cogVideoX/docker-compose.yaml`](../../../cogVideoX/docker-compose.yaml), and
the relevant implementation under `cogVideoX/src/cogvideox/` before diagnosing
or changing behavior.

## Run a generation

Use Docker Compose v2 from the repository root:

```sh
MODEL_ID=THUDM/CogVideoX-2b \
  docker compose -f cogVideoX/docker-compose.yaml up --build
```

The service generates a default-prompt video on startup. Set `MODEL_ID` to a
compatible text-to-video model before starting to select a different checkpoint.
Prompts are read from UTF-8 files in `cogVideoX/prompts/`; the CLI takes a file
path, never inline prompt text. Select a prompt file for Compose with
`PROMPT_FILE`:

```sh
PROMPT_FILE=/workspace/prompts/my-prompt.txt \
  docker compose -f cogVideoX/docker-compose.yaml up --build
```

The prompt directory is mounted read-only at `/workspace/prompts`. Use the
container path for `PROMPT_FILE` or `--prompt-file PATH`; host paths such as
`cogVideoX/prompts/my-prompt.txt` are not visible inside the container.

Generated output is written to `cogVideoX/output/`; downloaded model files use
the persistent `cogVideoX/cache/` bind mount. Do not remove either directory
when troubleshooting unless the user specifically requests it.

## Expected logs and lifecycle

Follow live logs or inspect a completed run:

```sh
docker compose -f cogVideoX/docker-compose.yaml logs -f --tail=100 cogvideo
docker compose -f cogVideoX/docker-compose.yaml ps -a
```

The application is a finite job, not a server. A successful run should log
CUDA availability, model loading, `MODEL LOADED`, generation preparation,
generation start, denoising progress, video encoding, and the saved output path.
The current generator reports every completed denoising step; step duration
varies with the model, hardware, and memory pressure. Once the video is written,
the process exits with status `0`. This stopped state is expected for a completed
generation; unlike Ollama, CogVideoX does not remain running after a job.

Loading logs can contain normal Hugging Face redirects, cache checks, warnings,
and model-download progress. CUDA usage can be observed with `nvidia-smi`.

## Troubleshooting procedure

1. Check `docker compose ... ps -a`, then review the full recent log context.
   Identify whether the run is downloading/loading, preparing inference,
   generating, encoding, or already complete.
2. If logs stop after `MODEL LOADED`, look for the generation-start message. If
   it is absent, verify the container command and image; rebuild and recreate
   after source changes because `src/` is baked into the image:

   ```sh
   docker compose -f cogVideoX/docker-compose.yaml up --build --force-recreate
   ```

3. If generation has started but progress is delayed, check whether inference
   is still active (`nvidia-smi` and container status). The progress callback
   runs only after a denoising step finishes, so a long first step can produce
   an apparent pause. Do not claim a hang from CPU/GPU utilization alone.
4. For model load or download failures, record the exact `MODEL_ID` and first
   underlying error. Check network/cache availability and available disk space.
   Use `HF_TOKEN` only when needed and never print or commit its value.
5. For CUDA out-of-memory or unsupported hardware, report the model, GPU,
   available memory, and traceback. Do not silently switch models or alter
   generation quality settings without user approval.
6. The current implementation uses `CogVideoXPipeline`, a text-to-video
   pipeline. Do not promise image-to-video checkpoint support (such as
   `...-I2V`) without verifying pipeline compatibility.
7. Report the command, exit code, relevant log lines, and whether the output
   file was created. Preserve model cache and generated output while diagnosing.

For library-development checks, use the `make test`, `make lint`, and
`make build` targets from `cogVideoX/`.
