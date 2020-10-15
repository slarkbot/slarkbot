
from . import request
from src.constants import API_URI_ENDPOINTS


def get_health_check():
    """
    returns response json and status code
    """
    uri = API_URI_ENDPOINTS.HEALTH_CHECK.value
    print(uri)
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_match_by_id(id):
    """
    takes in match id
    returns response json and status code
    """
    uri = API_URI_ENDPOINTS.MATCHES.value % id
    response = request.make_request(uri)
    return response.json(), response.status_code
