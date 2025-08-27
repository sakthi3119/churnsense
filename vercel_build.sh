#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Copy static files
cp -r static/* static/ 2>/dev/null || :

# Make sure the script has execute permissions
chmod +x vercel_build.sh
