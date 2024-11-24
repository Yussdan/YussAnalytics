"""
get /latest and /history data from external api
"""
from flask import Flask, jsonify
from utils.make_request import make_request
from api.config import api_key

app = Flask(__name__)

@app.route("/latest/<crypto>/<currency>", methods=["GET"])
def get_latest(crypto, currency):
    """
    get /latest data
    """
    params = {'fsym': crypto, 'tsyms': currency, 'api_key': api_key}
    data = make_request(endpoint='price', params=params)
    if "error" in data:
        return jsonify({"error": data["error"]}), 500
    return jsonify({crypto: f"{data[currency]} {currency}"}), 200

@app.route("/history/<crypto>/<time>/<currency>/<int:limit>", methods=["GET"])
def get_history(crypto, time, currency, limit):
    """
    get /history data
    """
    params = {'fsym': crypto, 'tsym': currency, 'limit': limit, 'api_key': api_key}
    data = make_request(endpoint=f"v2/histo{time}", params=params)
    if "error" in data:
        return jsonify({"error": data["error"]}), 500
    return jsonify(data['Data']['Data']), 200

if __name__ == "__main__":
    app.run(debug=False, port=5001)
