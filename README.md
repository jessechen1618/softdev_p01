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
Browse art from the Metropolitan Museum of Art in a more enhancing way!

## APIs used 
- [OpenCage Geocoder API](https://docs.google.com/document/d/1w6FLEo8vgAL-kqxjWVTemKhiq-YjGXltEsu7V34pERs/edit?usp=sharing)
- [Open Static Map API](https://docs.google.com/document/d/1Iwz9Y-7OM7KLxH0BLU1UOJUfYDMfiVOjfdQpDN2D6j4/edit?usp=sharing)
- [Met Museum Collections](https://docs.google.com/document/d/1ibirjeZ4Xv7Kf4XK0KFyVePFToN01PLum0lwTA5-RTA/edit?usp=sharing)
- [Imagga](https://docs.google.com/document/d/1rlxLfGuGFIJ13ac1FOr3LwlH_10Jsq8Vfe6aAZV4jYU/edit?usp=sharing)

## Instructions
**Assuming python3 and pip are already installed**
### Virtual Environment 
- To prevent conflicts with globally installed packages, it is recommended to run everything below in a virtual environment. 

Set up a virtual environment by running the following in your terminal:
```
python -m venv hero 
# replace hero with anything you want 
# If the above does not work, run with python3 (this may be the case if a version of python2 is also installed)
```

To enter your virtual environment, run the following:
```
. hero/bin/activate
```

To exit your virtual environment, run the following:
```
deactivate
```

### Dependencies 
Run the following line in your virtual environment
```
pip install -r doc/requirements.txt
```