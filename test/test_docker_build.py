#!/usr/bin/env python
import requests

# define constants
MAIN_APP = 'http://main-app:5000'
COURSE_APP = 'http://course-app:5000'
CHUNK_APP = 'http://chunk-app:5000'


def test_main_app():
    r = requests.get(MAIN_APP)
    assert r.status_code == 200


def test_course_app():
    r = requests.get(COURSE_APP)
    assert r.status_code == 200


def chunk_app():
    r = requests.get(CHUNK_APP)
    assert r.status_code == 200
