"""
API for Analyzing Cryptocurrency Data

This module provides an endpoint to analyze cryptocurrency data sent via POST requests. 
The analysis includes statistical metrics such as average, median, minimum, and maximum 
values based on the provided data.

Route:
    - /analytics: Accepts a JSON payload with cryptocurrency data and returns the analysis results.
"""
from flask import Flask, jsonify, request
from api.data_validation import validate_data

app = Flask(__name__)

@app.route("/analytics", methods=["POST"])
def analytics():
    """
    Analyze cryptocurrency data.

    This endpoint receives a JSON payload containing cryptocurrency data, validates it, 
    and computes basic statistical metrics. The metrics include:
        - Average closing price
        - Median closing price
        - Minimum low price
        - Maximum high price

    Returns:
        Response: A JSON object containing the calculated metrics:
            - "average" (float): Average of the 'close' prices.
            - "median" (float): Median of the 'close' prices.
            - "min" (float): Minimum of the 'low' prices.
            - "max" (float): Maximum of the 'high' prices.
        If validation fails, returns an error response with the appropriate status code.
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
