#!/bin/bash

# Exit on error
set -e

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

echo "Build completed successfully!"
