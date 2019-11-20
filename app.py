'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development 
2019-11-17
'''

from flask import Flask, request, redirect, session, render_template, url_for, flash
import urllib.request
import os
import json

imageurl ="https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
url = f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0"
req = urllib.request.Request(url)
req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
res = urllib.request.urlopen(req)
response = res.read()
data = json.loads(response)

app = Flask(__name__)
@app.route("/")
def root():
    return render_template(
        "login.html",
        title = "Login"
    )

if __name__ == "__main__":
    app.debug = True
    app.run()