FROM nvidia/cuda:12.1-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y python3 python3-pip git && \
    pip3 install --no-cache-dir vllm flask

# Set a working directory
WORKDIR /app

# Copy application files into the container
COPY app/ /app/

# Expose the port for the app
EXPOSE 5000

# Command to run the app
CMD ["python3", "main.py"]
