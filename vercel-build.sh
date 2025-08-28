#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Install Python 3.9 if not already installed
if ! command -v python3.9 &> /dev/null; then
    echo "Python 3.9 not found. Installing..."
    apt-get update && apt-get install -y python3.9 python3.9-venv
fi

# Create a virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies in the virtual environment
pip install -r requirements.txt

# Make sure the script has execute permissions
chmod +x vercel-build.sh

# Create a simple wsgi.py file if it doesn't exist
if [ ! -f wsgi.py ]; then
    echo "from app import app

if __name__ == "__main__":
    app.run()" > wsgi.py
fi
