"""
Module to fetch data from an external API.

This module provides functionality to send HTTP requests to an external API, 
specifically to the CryptoCompare API, to retrieve cryptocurrency data.

Dependencies:
- requests: Used for making HTTP requests to the API.
- logging: Used for logging errors and important events.

Functions:
- make_request: Sends a GET request to the specified endpoint and returns the response data in JSON format.
"""
import logging
import requests

logger = logging.getLogger('api')

def make_request(endpoint='', params=None, url='https://min-api.cryptocompare.com/data/'):
    """
    request to url + endpoint
    """
    try:
        response = requests.get(url + endpoint, params=params, timeout=100)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return {"error": str(e)}
