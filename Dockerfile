FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir runpod

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV FISH_SPEECH_MODEL_PATH=/runpod-volume/checkpoints/s2-pro
ENV LIVEPORTRAIT_MODEL_PATH=/runpod-volume/LivePortrait/models
ENV LTX_VIDEO_MODEL_PATH=/runpod-volume/LTX-Video

# Create app directories (NOT model dirs - those are on volume)
RUN mkdir -p /app/cache/scripts \
    && mkdir -p /app/cache/voices \
    && mkdir -p /app/cache/broll \
    && mkdir -p /app/cache/avatars \
    && mkdir -p /app/storage \
    && mkdir -p /app/temp \
    && mkdir -p /app/outputs

# RunPod serverless handler
CMD ["python", "handler.py"]
