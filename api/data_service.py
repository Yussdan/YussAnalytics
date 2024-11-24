"""
Cryptocurrency Data Fetcher API

This module provides endpoints to fetch real-time and historical cryptocurrency data 
from an external API. It uses a utility function `make_request` for making HTTP requests 
to the external API and handles error responses gracefully.

Routes:
    - /latest/<crypto>/<currency>: Fetches the latest price for the specified cryptocurrency in the given currency.
    - /history/<crypto>/<time>/<currency>/<int:limit>: Fetches historical price data for the specified cryptocurrency.

Dependencies:
    - `make_request`: A utility function for making HTTP requests.
    - `api_key`: The API key for accessing the external cryptocurrency API.
"""

from flask import Flask, jsonify
from utils.make_request import make_request
from api.config import api_key

app = Flask(__name__)

@app.route("/latest/<crypto>/<currency>", methods=["GET"])
def get_latest(crypto, currency):
    """
    Fetch the latest cryptocurrency price.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        currency (str): The fiat currency symbol (e.g., "USD").

    Returns:
        Response: A JSON object containing the latest price in the format:
            {
                "<crypto>": "<price> <currency>"
            }
        In case of an error, returns:
            {
                "error": "<error_message>"
            }
        with a status code of 500.
    """
    params = {'fsym': crypto, 'tsyms': currency, 'api_key': api_key}
    data = make_request(endpoint='price', params=params)
    if "error" in data:
        return jsonify({"error": data["error"]}), 500
    return jsonify({crypto: f"{data[currency]} {currency}"}), 200

@app.route("/history/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def get_history(crypto, time, currency, limit):
    """
    Fetch historical cryptocurrency price data.

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        time (str): The time interval for the historical data (e.g., "minute", "hour", "day").
        currency (str): The fiat currency symbol (e.g., "USD").
        limit (int): The number of historical records to fetch.

    Returns:
        Response: A JSON object containing the historical price data. The structure depends on 
        the external API's response. Example:
            [
                {"time": <timestamp>, "open": <price>, "close": <price>, ...},
                ...
            ]
        In case of an error, returns:
            {
                "error": "<error_message>"
            }
        with a status code of 500.
    """
    params = {'fsym': crypto, 'tsym': currency, 'limit': limit, 'api_key': api_key}
    data = make_request(endpoint=f"v2/histo{time}", params=params)
    if "error" in data:
        return jsonify({"error": data["error"]}), 500
    return jsonify(data['Data']['Data']), 200

if __name__ == "__main__":
    app.run(debug=False, port=5001)
