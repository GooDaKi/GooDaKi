#!/usr/bin/env python
import requests

# define constants
MAIN_APP = 'http://localhost:5000'
COURSE_APP = 'http://localhost:5001'
CHUNK_APP = 'http://localhost:5002'


def test_main_app():
    r = requests.get(MAIN_APP)
    assert r.status_code == 200


def test_course_app():
    r = requests.get(COURSE_APP)
    assert r.status_code == 200


def chunk_app():
    r = requests.get(CHUNK_APP)
    assert r.status_code == 200
