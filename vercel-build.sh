#!/bin/bash

# Exit on error
set -e

# Install system dependencies
apt-get update
apt-get install -y python3.9 python3.9-venv

# Create and activate virtual environment
python3.9 -m venv /tmp/venv
source /tmp/venv/bin/activate

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Make sure the script has execute permissions
chmod +x vercel-build.sh
