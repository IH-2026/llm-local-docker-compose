# Local AI Coding with Ollama

This repository provides a simple local AI stack for coding with Ollama and Docker Compose. It is designed for running open-source coding models such as Qwen2.5-Coder locally in VS Code, with optional NVIDIA GPU support and a Continue.dev integration. The default setup is a lightweight, reproducible Docker-based workflow that keeps model files and runtime state in a persistent local volume instead of relying on an external cloud service.

## Model overview

The cheat sheet focuses on the Qwen2.5-Coder family, which is well suited for local coding tasks such as code generation, autocomplete, and agent-style assistance. In practice:

- 1.5B: very fast and ideal for lightweight local work or laptops
- 3B: a good balance of speed and capability for coding assistance
- 7B: a strong default for local code generation and chat
- 14B: better for more complex agent workflows but needs more VRAM
- 32B: highest quality, but slower and requires more memory

A practical default for many developers is qwen2.5-coder:7b, which usually fits in about 8 GB of VRAM and works well for everyday development tasks.

## Docker Compose setup

The included [ollama/docker-compose.yml](ollama/docker-compose.yml) starts an Ollama container on port 11434 and keeps downloaded models in a Docker volume named `ollama`. This makes it easy to:

- start the local model server with `docker compose up -d`
- stop it with `docker compose down`
- keep models between sessions without re-downloading them
- enable NVIDIA GPU access for faster inference when the NVIDIA Container Toolkit is installed

The `ollama-pull` service is optional and can be used to auto-download models like `qwen2.5-coder:7b` and `qwen2.5-coder:3b` during setup.

## VS Code shortcuts and useful links

From the cheat sheet, the main VS Code shortcuts are:

- `Ctrl + L`: open Continue chat panel
- `Ctrl + I`: inline edit
- `Tab`: accept autocomplete
- `@workspace`: inject project context
- `@codebase`: inject the full codebase context
- `Ctrl + Shift + P` → `Continue: Reload Window`: reload the Continue config

Useful resources referenced in the PDF include:

- Ollama Docker Hub
- Ollama Models Library
- Ollama GitHub
- Continue.dev docs and config reference
- NVIDIA Container Toolkit install guide
- Qwen2.5-Coder on Hugging Face

## Useful NVIDIA commands

Use these commands to verify that the GPU is detected correctly and to monitor usage while running local models:

- `nvidia-smi` — general GPU status, temperature, utilization, and VRAM usage
- `lspci | grep -i nvidia` — check whether the NVIDIA GPU is visible to the system and identify the installed driver hardware
- `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv` — show concise GPU information, including model name, total memory, and driver version
- `watch -n 1 nvidia-smi` — refresh GPU statistics every second to monitor live load and memory usage

## Reference: cheat sheet sections 1-12

The full PDF is available here: [ollama/local-ai-coding-cheatsheet.pdf](ollama/local-ai-coding-cheatsheet.pdf)

1. Docker Compose Setup (GPU)
2. Alternative: Native Install (curl | sh)
3. Alternative: User-Local Install (No Sudo)
4. Alternative: Docker Run (One-Liner)
5. Continue.dev Config
6. Ollama Model Commands
7. Debug & Verify Commands
8. NVIDIA GPU Troubleshooting
9. VS Code Shortcuts
10. Useful Links
11. Model Size Reference
12. Hybrid Setup

This repository is a practical companion to that guide, focused on keeping a local coding workflow simple, reproducible, and ready for everyday development.
