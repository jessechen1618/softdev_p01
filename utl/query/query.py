import urllib.request
import base64
import json


def data(link, headers=False, auth=""):
    req = urllib.request.Request(link)  # create a request object
    # add headers only if necessary (for imagga)
    if headers:
        req.add_header(
            "Authorization", auth)
    res = urllib.request.urlopen(req)
    response = res.read()
    data = json.loads(response)
    return data
