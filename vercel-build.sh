#!/bin/bash

# Exit on error
set -e

# Set environment variables
export DEBIAN_FRONTEND=noninteractive
export PIP_ONLY_BINARY=:all:
export PIP_INDEX_URL=https://pypi.org/simple

# Install Python 3.9 and pip
apt-get update
apt-get install -y python3.9 python3-pip

# Create and activate virtual environment
python3.9 -m venv /tmp/venv
source /tmp/venv/bin/activate

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Make sure the script has execute permissions
chmod +x vercel-build.sh

# Verify Python version
python --version

# Verify installed packages
pip list