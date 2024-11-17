import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import sys
import io

from flask import Flask, jsonify
from dotenv import load_dotenv
from datetime import datetime

import matplotlib
matplotlib.use('Agg')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.s3_client import S3Client, make_request

load_dotenv()

api_key = os.getenv("api_key")
s3_key_id = os.getenv('s3_key_id')
s3_key_pass = os.getenv('s3_key_pass')


app = Flask(__name__)

@app.route("/<cryptocurrency>/latest/<current>", methods=["GET"])
def get_latest_prices(cryptocurrency, current):
    params = {'fsym': cryptocurrency, 'tsyms': current, 'api_key': api_key}
    data = make_request(endpoint='price', params=params)
    if "error" in data:
        return jsonify(data), 500
    return jsonify({cryptocurrency: f"{data[current]} {current}"})


@app.route("/<cryptocurrency>/<time>/<current>/<limit>", methods=["GET"])
def fetch_history_prices(cryptocurrency, time, current, limit):
    if time not in ['hour', 'day']:
        return {"error": "Invalid time parameter. Use 'hour' or 'day'."}, 400

    params = {'fsym': cryptocurrency, 'tsym': current, 'limit': limit, 'api_key': api_key}
    data = make_request(endpoint=f"v2/histo{time}", params=params)

    if "error" in data:
        return {"error": data.get("error", "Unknown error")}, 500

    prices = pd.DataFrame([
        {
            "time": datetime.fromtimestamp(info['time']).strftime('%H:%M' if time == 'hour' else '%Y-%m-%d'),
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
    data = fetch_history_prices(crypto, time, currency, limit)
    if isinstance(data, dict):
        return jsonify(data), data.get("status", 500)

    # Подготовка данных
    data['percent_change'] = data['close'].pct_change().fillna(0) * 100
    data['color'] = data['percent_change'].apply(lambda x: 'green' if x >= 0 else 'red')

    # Градиент цвета для линии
    colors = ['red', 'green']
    cmap = LinearSegmentedColormap.from_list('gradient', colors)

    # Построение графика
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(14, 8))

    # Линия с градиентом цвета
    for i in range(1, len(data)):
        ax.plot(
            [data['time'][i - 1], data['time'][i]],
            [data['close'][i - 1], data['close'][i]],
            color=cmap(data['percent_change'][i] / max(abs(data['percent_change']))),
            linewidth=2
        )

    # Добавление маркеров и текста с процентным изменением
    for i in range(len(data)):
        ax.scatter(data['time'][i], data['close'][i], color=data['color'][i], edgecolor='black', zorder=5)
        ax.text(
            data['time'][i], data['close'][i],
            f"{data['percent_change'][i]:+.2f}%",
            color='black',
            fontsize=8, ha='center', va='bottom'
        )

    # Заливка области под графиком
    ax.fill_between(data['time'], data['close'], color='blue', alpha=0.1)

    # Добавление заголовка и подписей
    ax.set_title(f"Price Trend for {crypto} ({limit} {time}s)", fontsize=16, fontweight='bold')
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Close Price", fontsize=12)

    min_close = data['close'].min()
    max_close = data['close'].max()
    padding = (max_close - min_close) * 0.05  # 5% от диапазона
    ax.set_ylim(min_close - padding, max_close + padding)

    # Автоматическое масштабирование оси времени
    ax.set_xlim(data['time'].iloc[0], data['time'].iloc[-1])

    # Настройка осей
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)

    # Добавление сетки
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Сохранение графика
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    try:
        resp=S3Client().upload_image(bucket='bucket-2490b3', local_file=buffer, bucket_file=f'{crypto}/{time}.png')
        return jsonify({'answer': resp}), 200
    except Exception as e:
        return jsonify({'answer': e}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)