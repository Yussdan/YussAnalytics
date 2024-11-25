# test_api.py
import requests

def test_get_latest():
    response = requests.get('http://localhost:5000/latest/BTC/USD')
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert 'BTC' in data

def test_get_history():
    response = requests.get('http://localhost:5000/history/BTC/day/USD/5"')
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert 'error' not in data

