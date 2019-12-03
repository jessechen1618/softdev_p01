import urllib.request
import base64
import json


def data(link, headers=False, auth=""):
    """
    Return data from REST API query

    Parameters:
        link (str): The link of the API query.
        headers (bool): A boolean representing whether or not authorization headers are needed for query.
        auth (str): A string containing authorization header.
    """
    req = urllib.request.Request(link)
    if headers:
        req.add_header("Authorization", auth)
    res = urllib.request.urlopen(req)
    response = res.read()
    data = json.loads(response)
    return data
