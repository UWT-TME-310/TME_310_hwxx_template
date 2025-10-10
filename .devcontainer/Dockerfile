# Use Microsoft's official Python 3.13 devcontainer base image
FROM mcr.microsoft.com/devcontainers/python:3.13

# Set working directory
WORKDIR /workspace

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to reduce image size
# Using pip install -U to ensure latest compatible versions
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-configure jupyter to reduce first-run setup time
RUN jupyter lab --generate-config || true

# Set environment variables for better Jupyter experience
ENV JUPYTER_ENABLE_LAB=yes

# The devcontainer will mount the workspace, so we don't need to keep requirements.txt in the image
RUN rm requirements.txt
