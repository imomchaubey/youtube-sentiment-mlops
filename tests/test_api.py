from fastapi.testclient import TestClient
from src.api.app import app
from src.data.clean_text import clean_text

client = TestClient(app)

def test_clean_text():
    sample = "Check out this video! http://example.com"
    cleaned = clean_text(sample)
    assert isinstance(cleaned, str)

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_predict_single_endpoint():
    response = client.post("/predict", json={"text": "This video is amazing!"})
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert data["sentiment"] in ["Positive", "Neutral", "Negative"]