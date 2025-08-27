#!/bin/bash

# Install Python 3.9
pyenv install 3.9.0
pyenv global 3.9.0

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Copy static files
cp -r static/* static/ 2>/dev/null || :

# Make sure the script has execute permissions
chmod +x vercel-build.sh
