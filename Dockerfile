# 1. Base image with Python, CUDA, and pip
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 2. Set environment variables for Python and prevent interactive issues
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install OS-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3.10-dev \
    git \
    cmake \
    ninja-build \
    build-essential \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Set python3.10 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# 5. Set working directory
WORKDIR /app

# 6. Copy all files into the container
COPY . /app

# 7. Upgrade pip and install Python dependencies (including torchmcubes)
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install git+https://github.com/tatsy/torchmcubes.git

# 8. Expose port (FastAPI runs on 8000 by default)
EXPOSE 8000

# 9. Entry point for FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
