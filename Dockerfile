FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set the working directory to /app as required by RunPod
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create required directories
RUN mkdir -p /app/checkpoints/s2-pro \
    && mkdir -p /app/LivePortrait/models \
    && mkdir -p /app/LTX-Video

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV FISH_SPEECH_MODEL_PATH=/app/checkpoints/s2-pro
ENV LIVEPORTRAIT_MODEL_PATH=/app/LivePortrait/models
ENV LTX_VIDEO_MODEL_PATH=/app/LTX-Video

# Create cache directories
RUN mkdir -p /app/cache/scripts \
    && mkdir -p /app/cache/voices \
    && mkdir -p /app/cache/broll \
    && mkdir -p /app/cache/avatars \
    && mkdir -p /app/storage \
    && mkdir -p /app/temp \
    && mkdir -p /app/outputs

# RunPod serverless handler
CMD ["python", "-m", "runpod.serverless", "--start_path", "handler.py"]
