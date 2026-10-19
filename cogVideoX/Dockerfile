FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# Hugging Face model cache
ENV HF_HOME=/workspace/cache/huggingface
ENV HUGGINGFACE_HUB_CACHE=/workspace/cache/huggingface/hub
ENV TRANSFORMERS_CACHE=/workspace/cache/huggingface/hub

# Reduce CUDA memory fragmentation
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade \
    pip \
    setuptools \
    wheel

# PyTorch for CUDA 12.4
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu124

# CogVideoX dependencies
RUN pip install --no-cache-dir \
    "diffusers>=0.30.1" \
    "transformers>=4.44.0" \
    "accelerate>=0.33.0" \
    "imageio>=2.34.0" \
    "imageio-ffmpeg>=0.5.1" \
    sentencepiece \
    protobuf

COPY pyproject.toml README.md /workspace/
COPY src /workspace/src
COPY prompts /workspace/prompts

RUN pip install --no-cache-dir --no-deps /workspace

RUN mkdir -p \
    /workspace/output \
    /workspace/cache

CMD ["python3", "-m", "cogvideox"]