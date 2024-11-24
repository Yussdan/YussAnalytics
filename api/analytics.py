"""
analyze data from api
"""
from flask import Flask, jsonify, request
from api.data_validation import validate_data

app = Flask(__name__)

@app.route("/analytics", methods=["POST"])
def analytics():
    """
    analyze data from api
    """
    df, error_response = validate_data(request.json)
    if error_response:
        return error_response

    return jsonify({
        "average": round(df['close'].mean(), 3),
        "median": round(df['close'].median(), 3),
        "min": round(df['low'].min(), 3),
        "max": round(df['high'].max(), 3),
    }), 200

if __name__ == "__main__":
    app.run(debug=False, port=5002)
