import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Flask app from the root app.py
from app import app

# This is required for Vercel
application = app

# This is the Vercel serverless function handler
def handler(event, context):
    # For Vercel Python runtime
    from vercel import Vercel
    vercel = Vercel(app)
    return vercel(event, context)

# This is for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
