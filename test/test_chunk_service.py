#!/usr/bin/env python
import requests
from bson.objectid import ObjectId

# define constants
CHUNK_APP = 'http://localhost:5002'
CHUNK_DB = 'http://localhost:28001'


def setup_function(func):
    print("setting up %s" % func)


def test_get_chunk_by_id(chunk_ids):
    for idx, (chunk_id, objs) in enumerate(chunk_ids):
        url = CHUNK_APP + '/api/chunk/' + chunk_id
        r = requests.get(url)
        assert r.status_code == 200
        assert r.json() == objs


def test_get_chunk_by_id_not_found():
    fake_id = '123456789012345678901234'
    url = CHUNK_APP + '/api/chunk/' + fake_id
    r = requests.get(url)
    assert r.status_code == 500


def test_get_chunk_by_id_invalid_id():
    wrong_id = 'xxx'  # too short
    url = CHUNK_APP + '/api/chunk/' + wrong_id
    r = requests.get(url)
    assert r.status_code == 400


def test_get_chunk_by_author_id(chunk_ids):
    author_ids = set(map(lambda x: x[1]['author_id'], chunk_ids))
    for aid in author_ids:
        url = CHUNK_APP + '/api/chunk/author/' + str(aid)
        r = requests.get(url)
        assert r.status_code == 200
        assert len(r.json()) != 0


def test_get_chunk_by_author_id_not_found():
    aid = 1000000000
    url = CHUNK_APP + '/api/chunk/author/' + str(aid)
    r = requests.get(url)
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_get_chunk_by_author_invalid_id():
    aid = 'invalid-id'
    url = CHUNK_APP + '/api/chunk/author/' + str(aid)
    r = requests.get(url)
    assert r.status_code == 400

#   TODO: write test for edit, create, search, delete
