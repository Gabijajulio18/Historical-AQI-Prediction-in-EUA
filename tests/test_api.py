from fastapi.testclient import TestClient
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.api.main import app

client = TestClient(app)


def test_root_endpoint():
    resp = client.get('/')
    assert resp.status_code == 200
    assert 'endpoints' in resp.json()


def test_predict_endpoint_sample_payload():
    with open('src/api/sample_payload.json') as f:
        payload = json.load(f)
    resp = client.post('/predict', json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert 'predictions' in data
    assert len(data['predictions']) == len(payload['data'])
