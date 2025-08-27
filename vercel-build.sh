#!/bin/bash

# Install Python 3.9
python3.9 -m pip install --upgrade pip

# Install build dependencies
pip install --upgrade setuptools wheel

# Install requirements
pip install -r requirements.txt --target .

# Create necessary directories
mkdir -p static

# Copy static files
cp -r static/* static/ 2>/dev/null || :

# Make sure the script has execute permissions
chmod +x vercel-build.sh
