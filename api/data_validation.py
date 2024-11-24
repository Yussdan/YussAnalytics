"""
Data Validation Utility

This module provides a utility function for validating and transforming cryptocurrency 
data fetched from an API. The data is converted into a Pandas DataFrame with a specific 
format based on the provided time interval.

Functionality:
    - Convert raw JSON data into a structured Pandas DataFrame.
    - Validate the presence of required fields and handle empty data gracefully.
"""

from datetime import datetime
import pandas as pd
from flask import jsonify

def validate_data(data, time=None):
    """
    Validate and transform cryptocurrency data.

    This function checks the integrity of the provided cryptocurrency data and 
    converts it into a structured Pandas DataFrame. It also formats the timestamp 
    into human-readable formats based on the specified time interval.

    Args:
        data (list[dict]): The raw cryptocurrency data to validate. Each dictionary 
                           represents a record with the fields:
                           - 'time' (int): Unix timestamp of the record.
                           - 'high' (float): The highest price during the interval.
                           - 'low' (float): The lowest price during the interval.
                           - 'close' (float): The closing price during the interval.
        time (str, optional): The time interval for formatting timestamps. Options:
                              - 'hour': Formats time as '%H:%M'.
                              - 'day': Formats time as '%Y-%m-%d'.
                              - None: Keeps the Unix timestamp as is.

    Returns:
        tuple:
            - pd.DataFrame: A structured DataFrame with columns ['time', 'high', 'low', 'close'].
            - Response: A Flask JSON response with an error message if the data is invalid.

    Example:
        Input:
            data = [
                {"time": 1698278400, "high": 100, "low": 95, "close": 98},
                {"time": 1698282000, "high": 102, "low": 97, "close": 100}
            ]
            time = 'hour'

        Output:
            pd.DataFrame({
                "time": ["00:00", "01:00"],
                "high": [100, 102],
                "low": [95, 97],
                "close": [98, 100]
            })

    Notes:
        - If the input data is empty, the function returns a Flask JSON error response.
    """
    df = pd.DataFrame([
        {
            "time": datetime.fromtimestamp(info['time']).strftime(
                '%H:%M' if time == 'hour' else '%Y-%m-%d' if time == 'day' else str(info['time'])),
            "high": info['high'],
            "low": info['low'],
            "close": info['close']
        }
        for info in data
    ])

    if df.empty:
        return None, jsonify({"error": "No data provided"})
    return df, None
