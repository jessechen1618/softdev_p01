import urllib.request
import base64
import json


def data(link, headers=False):
    req = urllib.request.Request(link)  # create a request object
    # add headers only if necessary (for imagga)
    if headers:
        req.add_header(
            "Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
    res = urllib.request.urlopen(req)
    response = res.read()
    data = json.loads(response)
    return data
