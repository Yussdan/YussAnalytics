"""
check data from api
"""
from datetime import datetime
import pandas as pd
from flask import jsonify

def validate_data(data, time=None):
    """
    Check and validate data.
    """
    df = pd.DataFrame([
    {
        "time": datetime.fromtimestamp(info['time']).strftime(
            '%H:%M' if time == 'hour' else '%Y-%m-%d' if time == 'day' else str(data['time'])),
        "high": info['high'],
        "low": info['low'],
        "close": info['close']
    }
    for info in data
    ])

    if df.empty:
        return None, jsonify({"error": "No data provided"})
    return df, None
