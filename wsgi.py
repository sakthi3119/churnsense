import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Flask app from api/index
from api.index import app as application

# This is required for Vercel
def handler(event, context):
    return application(event, context)

# This is for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=True)
