"""
pipeline.py - Unified Production Inference Pipeline for Vireo Audio Support Classification.
Ensures 100% code and model parity between training, evaluation, regression tests, and live Streamlit UI.
"""
import os
import joblib
from src.preprocessing import clean_text
from src.categorizer import VireoHybridClassifier, DomainIntentFeatures

# Default model path
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "vireo_classifier.joblib")

_CACHED_MODEL = None

def get_model(model_path=MODEL_PATH):
    """
    Load or return cached instance of the trained VireoHybridClassifier.
    """
    global _CACHED_MODEL
    if _CACHED_MODEL is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Trained model artifact not found at {model_path}. "
                "Please run `python run_eval.py` to train and serialize the production model."
            )
        _CACHED_MODEL = joblib.load(model_path)
    return _CACHED_MODEL

def predict_ticket(text, ticket_id="LIVE", model_path=MODEL_PATH):
    """
    Unified inference function used across all evaluation scripts, regression tests, and the live Streamlit dashboard.
    
    Returns structured dictionary matching prompt specification:
    - ticket_id
    - category (Primary predicted class)
    - subcategory (Granular root-cause driver)
    - confidence (Calibrated probability between 0.00 and 1.00)
    - second_best_category (Runner-up class)
    - second_best_confidence (Probability of runner-up)
    - margin (Confidence difference between top-1 and top-2)
    - review_required (Boolean gating supervisor review)
    - evidence (Extracted keywords/phrases justifying decision)
    - reason (Detailed rationale string)
    """
    cleaned = clean_text(text)
    model = get_model(model_path=model_path)
    result = model.predict_single(cleaned, ticket_id=ticket_id)
    return result
