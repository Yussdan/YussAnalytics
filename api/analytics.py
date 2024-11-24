from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

@app.route("/analytics", methods=["POST"])
def analytics():
    data = request.json  # Данные передаются из Data Service
    df = pd.DataFrame(data)

    if df.empty:
        return jsonify({"error": "No data provided"}), 400

    return jsonify({
        "average": df['close'].mean(),
        "median": df['close'].median(),
        "min": df['low'].min(),
        "max": df['high'].max(),
    }), 200

if __name__ == "__main__":
    app.run(debug=False, port=5002)
