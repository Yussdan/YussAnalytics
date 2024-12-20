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
from datetime import datetime
from flask import Flask, jsonify
import requests
from api.config import (
    DATA_SERVICE_URL,
    ANALYTICS_SERVICE_URL,
    PLOT_SERVICE_URL,
    TTL
)

app = Flask(__name__)

def fetch_data(url, timeout=TTL):
    """
    Универсальная функция для выполнения HTTP-запросов и обработки ошибок.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

@app.route("/latest/<crypto>/<currency>", methods=["GET"])
def latest(crypto, currency):
    """
    Fetch the latest cryptocurrency data.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        currency (str): The fiat currency symbol (e.g., "USD").
    Returns:
        Response: A JSON object containing 
        the latest cryptocurrency data and the corresponding status code.
    """
    url = f"{DATA_SERVICE_URL}/latest/{crypto}/{currency}"
    response = fetch_data(url)
    if response:
        return jsonify(response.json()), response.status_code
    return jsonify({"error": "Failed to fetch data"}), 500

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
        Response: A JSON object containing 
        the historical cryptocurrency data and the corresponding status code.
    """
    url = f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}"
    response = fetch_data(url)
    if response:
        return jsonify(response.json()), response.status_code
    return jsonify({"error": "Failed to fetch data"}), 500

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
    url = f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}"
    response = fetch_data(url)
    if response and response.status_code == 200:
        data = response.json()
        analytics_response = requests.post(
            f"{ANALYTICS_SERVICE_URL}/analytics", json=data, timeout=TTL)
        return jsonify(analytics_response.json()), analytics_response.status_code
    return jsonify({"error": "Failed to fetch data or perform analytics"}), 500

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
    url = f"{DATA_SERVICE_URL}/history/{crypto}/{time}/{currency}/{limit}"
    response = fetch_data(url)
    if response and response.status_code == 200:
        data = response.json()
        time_resp = datetime.now()
        plot_response = requests.post(
            f"{PLOT_SERVICE_URL}/plot/{crypto}/{time}/{time_resp}", json=data, timeout=TTL)
        return jsonify({'status':'success','time_resp':time_resp}), plot_response.status_code
    return jsonify({"error": "Failed to fetch data or generate plot"}), 500

if __name__ == "__main__":
    app.run(debug=False, port=5000)
