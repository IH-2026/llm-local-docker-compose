# Local AI Projects

This repository contains two independent projects for running generative AI
locally:

- **Ollama** — Run local language models, including Qwen2.5-Coder, for coding
  assistance. See the [Ollama setup guide](./ollama/README.md).
- **CogVideoX** — A Python library and CLI for generating videos with
  Hugging Face Diffusers CogVideoX models. See the
  [CogVideoX guide](./cogVideoX/README.md).

Each project has its own Docker Compose configuration and setup instructions.

## Agent skills
`
Repository-specific Copilot agent skills are available for operating and
troubleshooting each service:

- [Ollama local service skill](./.github/skills/ollama-local/SKILL.md)
- [CogVideoX local generator skill](./.github/skills/cogvideox-local/SKILL.md)