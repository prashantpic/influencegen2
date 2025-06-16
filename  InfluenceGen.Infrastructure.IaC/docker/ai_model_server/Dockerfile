# syntax=docker/dockerfile:1.4

# Use an NVIDIA CUDA base image for GPU support
# Choose tags based on required CUDA version, cuDNN version, and OS distribution
ARG CUDA_VERSION=12.1.0
ARG CUDNN_VERSION=8
ARG UBUNTU_VERSION=22.04
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-devel-ubuntu${UBUNTU_VERSION}

LABEL description="Docker image for InfluenceGen AI Model Serving with Flux LoRA support"

# Set environment variables for non-interactive apt install
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 # Ensure Python output is unbuffered

# Update package list and install basic tools and Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    git \
    curl \
    # Add any other system dependencies required by your AI app code
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the AI model serving application code into the container
# Assuming your app code is in a directory named 'ai_app_code' relative to the Dockerfile build context.
COPY ./ai_app_code/ /app/

# Install Python dependencies for the AI application
# Ensure PyTorch version is compatible with the CUDA version from the base image
# Note: For CUDA 12.1, the PyTorch index URL is often .../whl/cu121
RUN pip3 install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    diffusers transformers accelerate fastapi uvicorn[standard] \
    # Add any other Python libraries required by your application, e.g., specific Flux/LoRA libs
    # Example:
    # peft==0.8.2 # Or desired version
    # bitsandbytes==0.43.0 # Or desired version, if needed for quantization

# Copy model files into the image (Optional, consider using volumes for large models)
# COPY ./models/ /app/models/
# Alternative: Include a script to download models at runtime into a persistent volume

# Set the port the application listens on
ARG LISTEN_PORT=8000
EXPOSE ${LISTEN_PORT}

# Command to run the AI serving application
# Assuming your app uses FastAPI/Uvicorn and the main entry point is 'main:app'
# Use 'sh -c' to execute a command string that might involve environment variables or simple shell logic
CMD ["sh", "-c", "echo 'AI Server Starting...' && uvicorn main:app --host 0.0.0.0 --port ${LISTEN_PORT}"]

# Note: For production, use a specific, pinned base image tag (not just 'latest')
# and specify exact versions for all Python dependencies.
# Ensure your AI app code handles model loading, GPU utilization (e.g., .to('cuda')),
# and listens on 0.0.0.0 to be accessible externally from the container.