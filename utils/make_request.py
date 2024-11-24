import requests
import logging

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