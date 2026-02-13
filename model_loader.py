"""
Thread-safe singleton model loader for production ML deployments.
Handles cold starts, worker restarts, and prevents race conditions.
"""
import os
import joblib
import threading
from pathlib import Path
from typing import Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Thread-safe singleton lazy loader for ML models.
    
    Features:
    - Lazy loading: Model loads only when first needed
    - Thread-safe: Uses lock to prevent race conditions
    - Singleton: Only one instance across application
    - Absolute paths: Works reliably in production environments
    - Graceful error handling: Never crashes the application
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern: ensure only one instance exists."""
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking pattern
                if cls._instance is None:
                    cls._instance = super(ModelLoader, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the loader (only runs once due to singleton)."""
        if self._initialized:
            return
        
        self._model = None
        self._model_lock = threading.Lock()
        self._loading = False
        self._load_error = None
        self._initialized = True
        
        # Use absolute path based on this file's location
        base_dir = Path(__file__).resolve().parent
        self._model_path = base_dir / 'mlmodel.sav'
        
        logger.info(f"ModelLoader initialized. Model path: {self._model_path}")
    
    def get_model(self) -> Optional[Any]:
        """
        Get the loaded model. Loads automatically on first call.
        Thread-safe and prevents duplicate loading.
        
        Returns:
            The loaded model object, or None if loading failed.
        """
        # Fast path: model already loaded
        if self._model is not None:
            return self._model
        
        # Slow path: need to load model
        with self._model_lock:
            # Double-check: another thread might have loaded while we waited
            if self._model is not None:
                return self._model
            
            # Prevent recursive loading attempts
            if self._loading:
                logger.warning("Model is currently being loaded by another thread")
                return None
            
            self._loading = True
            try:
                self._load_model()
            finally:
                self._loading = False
            
            return self._model
    
    def _load_model(self):
        """Internal method to load the model from disk."""
        try:
            if not self._model_path.exists():
                error_msg = f"Model file not found: {self._model_path}"
                logger.error(error_msg)
                self._load_error = error_msg
                self._model = None
                return
            
            logger.info(f"Loading model from: {self._model_path}")
            
            self._model = joblib.load(self._model_path)
            
            logger.info("Model loaded successfully!")
            self._load_error = None
            
        except Exception as e:
            error_msg = f"Error loading model: {str(e)}"
            logger.error(error_msg)
            self._load_error = error_msg
            self._model = None
    
    def is_loaded(self) -> bool:
        """Check if model is successfully loaded."""
        return self._model is not None
    
    def is_loading(self) -> bool:
        """Check if model is currently being loaded."""
        return self._loading
    
    def get_error(self) -> Optional[str]:
        """Get the last loading error message, if any."""
        return self._load_error
    
    def reload(self):
        """Force reload the model from disk."""
        with self._model_lock:
            logger.info("Forcing model reload...")
            self._model = None
            self._load_error = None
            self._loading = True
            try:
                self._load_model()
            finally:
                self._loading = False
    
    def warm_up(self):
        """
        Warm up the model by loading it immediately.
        Safe to call at application startup.
        """
        logger.info("Warming up model loader...")
        self.get_model()


# Global singleton instance
_model_loader = ModelLoader()


def get_model():
    """
    Get the ML model (loads automatically on first call).
    
    Returns:
        The loaded model object, or None if loading failed.
    """
    return _model_loader.get_model()


def warm_up_model():
    """
    Warm up the model by loading it at application startup.
    Call this when your server initializes.
    """
    _model_loader.warm_up()


def is_model_ready() -> bool:
    """Check if model is loaded and ready for predictions."""
    return _model_loader.is_loaded()


def get_model_status() -> dict:
    """
    Get detailed model loading status.
    
    Returns:
        Dictionary with status information.
    """
    loader = _model_loader
    
    if loader.is_loaded():
        return {
            "status": "ready",
            "loaded": True,
            "loading": False,
            "error": None
        }
    elif loader.is_loading():
        return {
            "status": "loading",
            "loaded": False,
            "loading": True,
            "error": None
        }
    else:
        return {
            "status": "error" if loader.get_error() else "not_loaded",
            "loaded": False,
            "loading": False,
            "error": loader.get_error()
        }
