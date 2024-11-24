"""
centralizes API requests
"""
from flask import Flask, jsonify
import requests

app = Flask(__name__)

DATA_SERVICE_URL = "http://127.0.0.1:5001"
ANALYTICS_SERVICE_URL = "http://127.0.0.1:5002"
PLOT_SERVICE_URL = "http://127.0.0.1:5003"
TTL=40

@app.route("/latest/<crypto>/<currency>", methods=["GET"])
def latest(crypto, currency):
    """
    request latest data
    """
    response = requests.get(f"{DATA_SERVICE_URL}/latest/{crypto}/{currency}", timeout=TTL)
    return jsonify(response.json()), response.status_code

@app.route("/history/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def history(crypto, time, currency, limit):
    """
    request history data
    """
    response = requests.get(
        f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}", timeout=TTL)
    return jsonify(response.json()), response.status_code

@app.route("/analytics/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def analytics(crypto, time, currency, limit):
    """
    request analyze data
    """
    response = requests.get(
        f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}", timeout=TTL)
    if response.status_code != 200:
        return jsonify(response.json()), response.status_code

    data = response.json()
    response = requests.post(
        f"{ANALYTICS_SERVICE_URL}/analytics", json=data, timeout=TTL)
    return jsonify(response.json()), response.status_code

@app.route("/plot/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def plot(crypto, time, currency, limit):
    """
    request plot
    """
    response = requests.get(
        f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}", timeout=TTL)
    if response.status_code != 200:
        return jsonify(response.json()), response.status_code

    data = response.json()
    response = requests.post(
        f"{PLOT_SERVICE_URL}/plot/{crypto}/{time}", json=data, timeout=TTL)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(debug=False, port=5000)
