"""
module generate plot
"""
import io
import matplotlib.pyplot as plt
import matplotlib
from flask import Flask, jsonify, request

from utils.s3_client import S3Client
from api.data_validation import validate_data
from api.config import s3_key_id, s3_key_pass, bucket

matplotlib.use('Agg')

s3_client = S3Client(aws_access_key_id=s3_key_id, aws_secret_access_key=s3_key_pass)
app = Flask(__name__)

@app.route("/plot/<crypto>", methods=["POST"])
def generate_plot(crypto):
    """
    generate plot
    """
    df, error_response = validate_data(request.json)
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

    s3_path = f"{crypto}/plots/plot.png"
    resp = s3_client.upload_image(bucket=bucket, local_file=buffer, bucket_file=s3_path)
    return jsonify({'url': resp}), 200

if __name__ == "__main__":
    app.run(debug=False, port=5003)
