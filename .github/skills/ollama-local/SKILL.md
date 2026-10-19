---
name: ollama-local
description: "Use when starting, configuring, or troubleshooting this repository's Ollama Docker Compose service, Qwen coding models, API availability, container logs, or GPU usage."
---

# Ollama Local Service

Use this skill for the persistent Ollama server in `ollama/`. Read
[`ollama/README.md`](../../../ollama/README.md) and
[`ollama/docker-compose.yml`](../../../ollama/docker-compose.yml) for the
current setup before changing or diagnosing it.

## Start and stop

Run commands from the repository root with Docker Compose v2:

```sh
docker compose -f ollama/docker-compose.yml up -d ollama
docker compose -f ollama/docker-compose.yml ps
docker compose -f ollama/docker-compose.yml down
```

The service is intended to stay running and serves its API on port `11434`.
Its named `ollama` volume persists downloaded models.

Pull a model into the running server:

```sh
docker compose -f ollama/docker-compose.yml exec ollama ollama pull qwen2.5-coder:7b
docker compose -f ollama/docker-compose.yml exec ollama ollama pull qwen2.5-coder:3b
```

The optional `ollama-pull` setup profile declares
`depends_on: condition: service_healthy`. The Compose file has no explicit
healthcheck, so verify the image's health status and dependency behavior before
relying on that profile. Prefer the explicit pull commands above if it does not
start as expected.

## Read logs and verify the API

```sh
docker compose -f ollama/docker-compose.yml logs -f --tail=100 ollama
curl -fsS http://localhost:11434/api/tags
docker compose -f ollama/docker-compose.yml exec ollama ollama list
```

Expected behavior:

- The Ollama container remains running; it is a server, not a one-shot job.
- `ollama list` shows locally available models. A model pull logs download
  progress and completes before the model is listed.
- The API tags endpoint responds with JSON, including an empty model list if
  no models have been pulled yet.
- GPU usage is optional; verify it with `nvidia-smi` while a model is running.

## Troubleshooting procedure

1. Check service state with `docker compose ... ps -a`; read recent service
   output with `docker compose ... logs --tail=200 ollama`.
2. If the container is stopped or restarting, identify the first error in its
   logs before changing configuration. Check Docker daemon health and port
   `11434` conflicts.
3. If the API check fails, confirm the container is running and port `11434` is
   published. Do not expose the service publicly unless the user asks.
4. If a model is missing, inspect `ollama list` and pull the exact model tag.
   Model files persist in the named volume; avoid deleting volumes as a
   troubleshooting shortcut.
5. If GPU access fails, verify host NVIDIA drivers and NVIDIA Container Toolkit,
   then inspect container logs. Keep CPU/GPU behavior claims grounded in actual
   runtime output.
6. Report the failing command, relevant log lines, container status, and API
   check result. Redact credentials and tokens from logs before sharing.
