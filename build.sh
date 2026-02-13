#!/bin/bash

# Exit on error
set -e

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (force reinstall to avoid cache issues)
pip install --no-cache-dir --force-reinstall -r requirements.txt

# Install in development mode
pip install -e .

echo "Build completed successfully!"
echo "Python version: $(python --version)"
echo "Scikit-learn version: $(python -c 'import sklearn; print(sklearn.__version__)')"
