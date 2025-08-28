import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Import the Flask app
from app import app

# This is required for Vercel
app = app

# This is the Vercel serverless function handler
# It will be used when the app is deployed on Vercel
def handler(request, context):
    return app(request.environ, lambda status, headers: [])

# This is for local development
if __name__ == "__main__":
    app.run(debug=True)
