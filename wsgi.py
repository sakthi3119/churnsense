import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Flask app and warm up model
from app import app as application
from model_loader import warm_up_model

# Warm up model immediately for production servers (Gunicorn, uWSGI, etc.)
logger.info("WSGI: Warming up model on worker startup...")
warm_up_model()
logger.info("WSGI: Model warm-up completed!")

# This is required for Vercel
def handler(event, context):
    return application(event, context)

# This is for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=True)
