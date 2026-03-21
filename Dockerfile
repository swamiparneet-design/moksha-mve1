FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/workspace
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# Default command
CMD ["python", "-m", "runpod.serverless", "--start_path", "handler.py"]
