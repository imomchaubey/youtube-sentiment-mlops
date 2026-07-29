import os
from typing import List
import joblib
import nltk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.data.clean_text import clean_text

# Ensure NLTK stopwords are downloaded on app startup
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

app = FastAPI(title="YouTube Sentiment Analysis API", version="1.0")

# Enable CORS so the Chrome Extension can talk to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "src/models/sentiment_pipeline.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}. Run training first!")

model = joblib.load(MODEL_PATH)

SENTIMENT_MAP = {
    -1.0: "Negative",
     0.0: "Neutral",
     1.0: "Positive"
}

# --- Request / Response Schemas ---
class SingleCommentRequest(BaseModel):
    text: str

class BatchCommentRequest(BaseModel):
    comments: List[str]

# --- Endpoints ---
@app.get("/")
def home():
    return {"status": "online", "message": "YouTube Sentiment API is active!"}

@app.post("/predict")
def predict_single(request: SingleCommentRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    cleaned = clean_text(request.text)
    prediction = model.predict([cleaned])[0]
    sentiment = SENTIMENT_MAP.get(float(prediction), "Unknown")
    
    return {
        "text": request.text,
        "cleaned_text": cleaned,
        "sentiment": sentiment,
        "label": float(prediction)
    }

@app.post("/predict_batch")
def predict_batch(request: BatchCommentRequest):
    if not request.comments:
        raise HTTPException(status_code=400, detail="Comment list cannot be empty.")
    
    cleaned_texts = [clean_text(c) for c in request.comments]
    predictions = model.predict(cleaned_texts)
    
    results = []
    summary = {"Positive": 0, "Neutral": 0, "Negative": 0}
    
    for original, cleaned, pred in zip(request.comments, cleaned_texts, predictions):
        sentiment = SENTIMENT_MAP.get(float(pred), "Unknown")
        if sentiment in summary:
            summary[sentiment] += 1
        
        results.append({
            "text": original,
            "sentiment": sentiment,
            "label": float(pred)
        })
        
    return {
        "total_comments": len(request.comments),
        "summary": summary,
        "results": results
    }