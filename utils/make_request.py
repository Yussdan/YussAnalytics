"""
Module to fetch data from an external API.

This module provides functionality to send HTTP requests to an external API, 
specifically to the CryptoCompare API, to retrieve cryptocurrency data.

Dependencies:
- requests: Used for making HTTP requests to the API.
- logging: Used for logging errors and important events.

Functions:
- make_request: Sends a GET request to the specified 
            endpoint and returns the response data in JSON format.
"""
import logging
import requests

logger = logging.getLogger('api')

def make_request(endpoint='', params=None, url='https://min-api.cryptocompare.com/data/'):
    """
    Sends a GET request to the specified API endpoint and returns the JSON response.

    This function constructs a URL by combining the base URL and the provided endpoint, 
    sends a GET request with optional parameters, 
        and returns the response data in JSON format.
    If an error occurs during the request, 
        it logs the error and returns an error message.

    Args:
        endpoint (str): The API endpoint to send the request to.
        params (dict, optional): A dictionary of query parameters 
            to include in the request.
        url (str): The base URL of the API.

    Returns:
        dict: A dictionary containing the response data in JSON format 
            or an error message.
        If the request is successful, returns the JSON data from the response.
        If the request fails, returns a dictionary with an 'error' 
            key containing the error message.
    """
    try:
        response = requests.get(url + endpoint, params=params, timeout=100)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return {"error": str(e)}
