"""
check data from api
"""
from datetime import datetime
import pandas as pd
from flask import jsonify

import pandas as pd
from datetime import datetime

def validate_data(data, time=None):
    """
    Check and validate data.
    """
    df = pd.DataFrame([
    {
        "time": datetime.fromtimestamp(data['time']).strftime(
            '%H:%M' if time == 'hour' else '%Y-%m-%d' if time == 'day' else str(data['time'])
        ),
        "high": data['high'],
        "low": data['low'],
        "close": data['close']
    }
    ])

    if df.empty:
        return None, jsonify({"error": "No data provided"})
    return df, None
