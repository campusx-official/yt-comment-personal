import pytest
import requests
import json

BASE_URL = "http://localhost:5000"  # Replace with your deployed URL if needed

def test_predict_endpoint():
    data = {
        "comments": ["This is a great product!", "Not worth the money.", "It's okay."]
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_predict_with_timestamps_endpoint():
    data = {
        "comments": [
            {"text": "This is fantastic!", "timestamp": "2024-10-25 10:00:00"},
            {"text": "Could be better.", "timestamp": "2024-10-26 14:00:00"}
        ]
    }
    response = requests.post(f"{BASE_URL}/predict_with_timestamps", json=data)
    assert response.status_code == 200
    assert all('sentiment' in item for item in response.json())

def test_generate_chart_endpoint():
    data = {
        "sentiment_counts": {"1": 5, "0": 3, "-1": 2}
    }
    response = requests.post(f"{BASE_URL}/generate_chart", json=data)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"

def test_generate_wordcloud_endpoint():
    data = {
        "comments": ["Love this!", "Not so great.", "Absolutely amazing!", "Horrible experience."]
    }
    response = requests.post(f"{BASE_URL}/generate_wordcloud", json=data)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"

def test_generate_trend_graph_endpoint():
    data = {
        "sentiment_data": [
            {"timestamp": "2024-10-01", "sentiment": 1},
            {"timestamp": "2024-10-02", "sentiment": 0},
            {"timestamp": "2024-10-03", "sentiment": -1}
        ]
    }
    response = requests.post(f"{BASE_URL}/generate_trend_graph", json=data)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
