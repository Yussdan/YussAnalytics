"""
check data from api
"""
import pandas as pd
from flask import jsonify

def validate_data(data):
    """
    check data
    """
    df = pd.DataFrame(data)
    if df.empty:
        return None, jsonify({"error": "No data provided"}), 400
    return df, None
