# ArtPI by put_me_to_REST

## Roster

- **Jesse "McCree" Chen** (PM):
  - Design document, project flow, coding here and there
- **Kelvin Ng**:
  - Back-end database and front-end implementation of Met API
- **Eric "Morty" Lau**:
  - Full-stack, CSS, Bootstrap, database, Implementation of Imagga API
- **David Xiedeng**:
  - Back-end database and front-end implementation of Map Static API

## Description

Browse art from the Metropolitan Museum of Art in a more enhancing way! Our website allows users to browse the Metropolitan Museum of Art's collection and interact with the art. Users can save their favorite artworks, comment on them, search by multiple categories, find information about the art, locate the art's creation place, and identify the color palette. This is done via the interaction of many APIs which is detailed below.

## APIs used

- [Open Static Map API](https://docs.google.com/document/d/1Iwz9Y-7OM7KLxH0BLU1UOJUfYDMfiVOjfdQpDN2D6j4/edit?usp=sharing)
- [Met Museum Collections](https://docs.google.com/document/d/1ibirjeZ4Xv7Kf4XK0KFyVePFToN01PLum0lwTA5-RTA/edit?usp=sharing)
- [Imagga](https://docs.google.com/document/d/1rlxLfGuGFIJ13ac1FOr3LwlH_10Jsq8Vfe6aAZV4jYU/edit?usp=sharing)

## Instructions

### Assuming python3 and pip are already installed

### Virtual Environment

- To prevent conflicts with globally installed packages, it is recommended to run everything below in a virtual environment.

Set up a virtual environment by running the following in your terminal:

```shell
python -m venv hero
# replace hero with anything you want
# If the above does not work, run with python3 (this may be the case if a version of python2 is also installed)
```

To enter your virtual environment, run the following:

```shell
. hero/bin/activate
```

To exit your virtual environment, run the following:

```shell
deactivate
```

### Dependencies

Run the following line in your virtual environment

```shell
pip install -r doc/requirements.txt
```

### Launch codes

Open app.py and add your MapQuest API key and your Imagga Authorization Header.

```python
MAPQUEST_API_KEY = "" # INSERT MAPQUEST API KEY HERE
IMAGGA_AUTH = "" # INSERT IMAGGA AUTHORIZATION HEADER HERE
```

### Running

Run the following line in your virtual environment

```shell
python app.py
```

Open a browser and head to <http://127.0.0.1:5000/>
