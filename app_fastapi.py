"""
FastAPI alternative implementation with the same model loader.
To use this instead of Flask, rename this to app.py or update your deployment config.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from typing import Optional
import numpy as np
from datetime import datetime
from pathlib import Path
from model_loader import get_model, warm_up_model, is_model_ready, get_model_status

app = FastAPI(title="ChurnSense API", version="1.0.0")

# Mount static files and templates
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"

if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

templates = Jinja2Templates(directory=str(templates_path))

# Feature names for reference
FEATURE_NAMES = ['contract', 'totalcharges', 'onlinesecurity', 'techsupport', 'internetservice']


# Pydantic models for request/response validation
class PredictionRequest(BaseModel):
    contract: float
    totalcharges: float
    onlinesecurity: float
    techsupport: float
    internetservice: float
    
    @validator('contract', 'totalcharges', 'onlinesecurity', 'techsupport', 'internetservice')
    def validate_numeric(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Must be a numeric value')
        return float(v)


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    churn_probability: float
    features: dict
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    error: Optional[str] = None


# Startup event to warm up model
@app.on_event("startup")
async def startup_event():
    """Load model when application starts."""
    warm_up_model()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint.
    Returns status of model loading.
    """
    status = get_model_status()
    
    if status['status'] == 'ready':
        return JSONResponse(
            status_code=200,
            content={"status": "ready"}
        )
    elif status['status'] == 'loading':
        return JSONResponse(
            status_code=503,
            content={"status": "loading"}
        )
    else:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "error": status.get('error', 'Model not loaded')
            }
        )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make a churn prediction based on customer features.
    """
    # Get model (loads automatically if not yet loaded)
    model = get_model()
    
    # Check if model is loaded
    if model is None:
        status = get_model_status()
        error_message = status.get('error', 'Model not loaded. Please try again later.')
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Model not available",
                "details": error_message,
                "status": status['status']
            }
        )
    
    try:
        # Extract features
        features = np.array([
            request.contract,
            request.totalcharges,
            request.onlinesecurity,
            request.techsupport,
            request.internetservice
        ]).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        confidence = max(prediction_proba) * 100
        
        # Get the probability of churn (class 1)
        churn_probability = prediction_proba[1] * 100
        
        # Map prediction to readable output
        prediction_text = ("The customer is more likely to churn" 
                         if prediction == 1 
                         else "The customer is likely to stay")
        
        # Prepare response
        response = {
            "prediction": prediction_text,
            "confidence": round(confidence, 2),
            "churn_probability": round(churn_probability, 2),
            "features": {
                "contract": {
                    "value": request.contract,
                    "label": get_contract_label(request.contract)
                },
                "total_charges": float(request.totalcharges),
                "online_security": get_yes_no_label(request.onlinesecurity),
                "tech_support": get_yes_no_label(request.techsupport),
                "internet_service": get_internet_service_label(request.internetservice)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "An error occurred while processing your request.",
                "details": str(e)
            }
        )


# Helper functions for label mapping
def get_contract_label(value):
    mapping = {
        1: "Month-to-month", "1": "Month-to-month",
        2: "One year", "2": "One year",
        3: "Two year", "3": "Two year"
    }
    return mapping.get(value, mapping.get(str(value), "Unknown"))


def get_yes_no_label(value):
    value_str = str(value)
    if value_str == "0" or value == 0:
        return "No"
    elif value_str == "1" or value == 1:
        return "Yes"
    elif value_str == "2" or value == 2:
        return "No internet service"
    return "Unknown"


def get_internet_service_label(value):
    mapping = {
        0: "No internet service", "0": "No internet service",
        1: "DSL", "1": "DSL",
        2: "Fiber optic", "2": "Fiber optic"
    }
    return mapping.get(value, mapping.get(str(value), "Unknown"))


# For Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
