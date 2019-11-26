import urllib.request
import base64
import json

def data(link, headers=False, mapquest=False):
    req = urllib.request.Request(link) ## create a request object
    # add headers only if necessary (for imagga)
    if headers: req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
    res = urllib.request.urlopen(req)
    response = res.read()
    if mapquest:
         # altResponse =  base64.b64decode(response).decode('utf-8')
         # altResponse = open(response, encoding = "ISO-8859-1")
         print("this is what it prints", response)
         # print("alternate response", altResponse)
         return response
    data = json.loads(response)
    return data
