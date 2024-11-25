"""
Plot Generation Module

This module provides an API endpoint to generate and upload cryptocurrency price trend plots. 
It uses Matplotlib for generating plots and uploads the resulting images to an S3 bucket.

Functionality:
    - Validate and preprocess cryptocurrency data.
    - Generate a time-series plot of close prices.
    - Upload the generated plot image to an S3 bucket.

Dependencies:
    - `S3Client`: Utility for interacting with AWS S3.
    - `validate_data`: Function to validate and preprocess input data.
    - `matplotlib`: Library for creating visualizations.

Routes:
    - /plot/<crypto>/<time> [POST]: Accepts JSON data to generate a plot and uploads it to S3.
"""
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib
from flask import Flask, jsonify, request

from utils.s3_client import S3Client
from api.data_validation import validate_data
from api.config import s3_key_id, s3_key_pass, bucket

matplotlib.use('Agg')  # Use non-interactive backend for server-side rendering

s3_client = S3Client(aws_access_key_id=s3_key_id, aws_secret_access_key=s3_key_pass)
app = Flask(__name__)

@app.route("/plot/<crypto>/<time>/<time_resp>", methods=["POST"])
def generate_plot(crypto, time, time_resp):
    """
    Generate and upload a cryptocurrency price trend plot.

    This endpoint takes cryptocurrency price data as JSON, generates a time-series plot 
    of close prices, and uploads the resulting image to an S3 bucket. 

    Args:
        crypto (str): The cryptocurrency symbol (e.g., "BTC").
        time (str): The time interval for the plot (e.g., "hour", "day").

    Input:
        JSON payload containing an array of data records with the fields:
        - 'time' (int): Unix timestamp of the record.
        - 'close' (float): The closing price during the interval.

    Returns:
        Response: 
        - On success: JSON object with the URL of the uploaded plot:
            {
                "url": "<S3_bucket_url>"
            }
        - On failure: JSON error message with appropriate HTTP status code.

    Example:
        Request:
            POST /plot/BTC/hour
            JSON payload:
            [
                {"time": 1698278400, "close": 9800},
                {"time": 1698282000, "close": 9900}
            ]

        Response:
            {
                "url": "https://s3.amazonaws.com/<bucket>/BTC/plots/plot.png"
            }

    Notes:
        - The plot includes:
            * X-axis: Time (formatted based on the specified interval).
            * Y-axis: Closing price.
            * Title: "Price Trend".
        - The plot is saved in PNG format and uploaded to the specified S3 bucket.
    """
    time_resp = datetime.strptime(time_resp, '%Y-%m-%d %H:%M:%S.%f')
    date_part = time_resp.strftime('%Y-%m-%d')
    time_part = time_resp.strftime('%H:%M')
    s3_path = f"{date_part}/{time_part}/plot.png"
    df, error_response = validate_data(request.json, time)
    if error_response:
        return error_response

    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['close'], marker='o')
    plt.xlabel("Time")
    plt.ylabel("Close Price")
    plt.title("Price Trend")
    plt.grid()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    resp = s3_client.upload_image(bucket=bucket, local_file=buffer, bucket_file=s3_path)
    return jsonify({'url': resp}), 200

if __name__ == "__main__":
    app.run(debug=False, port=5003)
