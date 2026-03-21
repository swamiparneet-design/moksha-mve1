FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set the working directory to /workspace
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create required directories
RUN mkdir -p /workspace/checkpoints/s2-pro \
    && mkdir -p /workspace/LivePortrait/models \
    && mkdir -p /workspace/LTX-Video

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/workspace
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV FISH_SPEECH_MODEL_PATH=/workspace/checkpoints/s2-pro
ENV LIVEPORTRAIT_MODEL_PATH=/workspace/LivePortrait/models
ENV LTX_VIDEO_MODEL_PATH=/workspace/LTX-Video

# Create cache directories
RUN mkdir -p /workspace/cache/scripts \
    && mkdir -p /workspace/cache/voices \
    && mkdir -p /workspace/cache/broll \
    && mkdir -p /workspace/cache/avatars \
    && mkdir -p /workspace/storage \
    && mkdir -p /workspace/temp \
    && mkdir -p /workspace/outputs

# RunPod serverless handler
CMD ["python", "-m", "runpod.serverless", "--start_path", "handler.py"]
