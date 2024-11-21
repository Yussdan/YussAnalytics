"""
api cripto
"""

import os
import io
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from flask import Flask, jsonify
from dotenv import load_dotenv
from datetime import datetime
from utils.s3_client import S3Client, make_request

matplotlib.use('Agg')

load_dotenv()

api_key = os.getenv("api_key")
s3_key_id = os.getenv('s3_key_id')
s3_key_pass = os.getenv('s3_key_pass')

app = Flask(__name__)

@app.route("/<cryptocurrency>/latest/<current>", methods=["GET"])
def get_latest_prices(cryptocurrency, current):
    """
    return last prices
    """
    params = {'fsym': cryptocurrency, 'tsyms': current, 'api_key': api_key}
    data = make_request(endpoint='price', params=params)
    if "error" in data:
        return jsonify(data), 500
    return jsonify({cryptocurrency: f"{data[current]} {current}"})


@app.route("/<cryptocurrency>/<time>/<current>/<limit>", methods=["GET"])
def fetch_history_prices(cryptocurrency, time, current, limit):
    """
    return history data
    """
    if time not in ['hour', 'day']:
        return {"error": "Invalid time parameter. Use 'hour' or 'day'."}, 400

    params = {'fsym': cryptocurrency, 'tsym': current, 'limit': limit, 'api_key': api_key}
    data = make_request(endpoint=f"v2/histo{time}", params=params)

    if "error" in data:
        return {"error": data.get("error", "Unknown error")}, 500

    prices = pd.DataFrame([
        {
            "time": datetime.fromtimestamp(info['time']).strftime(
                '%H:%M' if time == 'hour' else '%Y-%m-%d'),
            "high": info['high'],
            "low": info['low'],
            "close": info['close']
        }
        for info in data.get('Data', {}).get('Data', [])
    ])

    if prices.empty:
        return {"error": "No data returned for the given parameters."}, 404

    return prices



@app.route("/<crypto>/analytics/<currency>/<time>/<limit>", methods=["GET"])
def get_analytics(crypto, time, currency, limit):
    """
    return data
    """
    data = fetch_history_prices(crypto, time, currency, limit)
    if isinstance(data, dict):
        return jsonify(data), data.get("status", 500)
    return jsonify({
        "average": data['close'].mean(),
        "median": data['close'].median(),
        "min": data['low'].min(),
        "max": data['high'].max(),
    })


@app.route("/<crypto>/plot/<currency>/<time>/<limit>", methods=["GET"])
def get_plot(crypto, time, currency, limit):
    """
    return plot
    """
    data = fetch_history_prices(crypto, time, currency, limit)
    if isinstance(data, dict):
        return jsonify(data), data.get("status", 500)

    data['percent_change'] = data['close'].pct_change().fillna(0) * 100
    data['color'] = data['percent_change'].apply(lambda x: 'green' if x >= 0 else 'red')

    plt.figure(figsize=(12, 6))

    for i in range(1, len(data)):
        plt.plot(
            [data['time'][i - 1], data['time'][i]],
            [data['close'][i - 1], data['close'][i]],
            color=data['color'][i],
            linewidth=2.5
        )

        plt.text(
            data['time'][i],
            data['close'][i],
            f"{data['percent_change'][i]:+.2f}%",
            color='black',
            ha='center', va='bottom', fontsize=9,
            bbox={'facecolor':data['color'][i], 
                      'alpha':0.3, 'edgecolor':None, 'boxstyle':round,'pad':0.3}
        )

    plt.xlabel("Time")
    plt.ylabel("Close Price")
    plt.title(f"Price Trend for {crypto} ({limit} {time}s)", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    try:
        resp=S3Client().upload_image(bucket='bucket-2490b3', local_file=buffer, bucket_file=f'{crypto}/{time}.png')
        return jsonify({'answer': resp}), 200
    except Exception as e:
        return jsonify({'answer': e}), 500


@app.errorhandler(404)
def not_found():
    """
    return error
    """
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
