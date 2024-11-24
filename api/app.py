"""
Centralized API Gateway

This module provides an API gateway to centralize requests to various services such as:
- Data Service: Provides real-time and historical cryptocurrency data.
- Analytics Service: Analyzes cryptocurrency trends based on historical data.
- Plot Service: Generates plots for cryptocurrency trends.

Routes:
    - /latest/<crypto>/<currency>: Fetch the latest cryptocurrency data.
    - /history/<crypto>/<time>/<currency>/<int:limit>: Fetch historical cryptocurrency data.
    - /analytics/<crypto>/<time>/<currency>/<int:limit>: Perform analytics on historical data.
    - /plot/<crypto>/<time>/<currency>/<int:limit>: Generate plots for cryptocurrency data.
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
    Fetch the latest cryptocurrency data.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        currency (str): The fiat currency symbol (e.g., "USD").

    Returns:
        Response: A JSON object containing the latest cryptocurrency data and the corresponding status code.
    """
    response = requests.get(f"{DATA_SERVICE_URL}/latest/{crypto}/{currency}", timeout=TTL)
    return jsonify(response.json()), response.status_code

@app.route("/history/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def history(crypto, time, currency, limit):
    """
    Fetch historical cryptocurrency data.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        time (str): The time period for historical data (e.g., "1h", "1d").
        currency (str): The fiat currency symbol (e.g., "USD").
        limit (int): The maximum number of records to fetch.

    Returns:
        Response: A JSON object containing the historical cryptocurrency data and the corresponding status code.
    """
    response = requests.get(
        f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}", timeout=TTL)
    return jsonify(response.json()), response.status_code

@app.route("/analytics/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def analytics(crypto, time, currency, limit):
    """
    Perform analytics on historical cryptocurrency data.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        time (str): The time period for historical data (e.g., "1h", "1d").
        currency (str): The fiat currency symbol (e.g., "USD").
        limit (int): The maximum number of records to analyze.

    Returns:
        Response: A JSON object containing the analytics results and the corresponding status code.
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
    Generate a plot for cryptocurrency trends.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        time (str): The time period for historical data (e.g., "1h", "1d").
        currency (str): The fiat currency symbol (e.g., "USD").
        limit (int): The maximum number of records to use for plotting.

    Returns:
        Response: A JSON object containing the plot image data and the corresponding status code.
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
