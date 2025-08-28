import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Import the Flask app
from app import app

# This is required for Vercel
application = app

# This is the Vercel serverless function handler
def handler(request, context):
    return application(request.environ, lambda status, headers: [])

# This is for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=True)
