# Use an official Python 3.12 base image
FROM mcr.microsoft.com/devcontainers/python:3.12

# Set working directory
WORKDIR /workspace

# Copy requirements.txt and install dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Copy custom .bashrc
COPY .bashrc /home/vscode/.bashrc
RUN chown vscode:vscode /home/vscode/.bashrc

# Default user
USER vscode
