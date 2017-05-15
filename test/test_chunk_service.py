#!/usr/bin/env python
import requests
import copy

# define constants
CHUNK_APP = 'http://localhost:5002'
CHUNK_DB = 'http://localhost:28001'


# def setup_function(func):
# print("setting up %s" % func)

def get_valid_payload():
    payload = {
        'author_id': 23,
        'name': 'cutting a wood',
        'description': 'learning how to cut firewood',
        'type': 'text',
        'text': 'first pick up some wood then ...',
        'created': '2012-12-31 23:59:59',
        'updated': '2012-12-31 23:59:59',
        'tags': ['tag-1', 'tag-2']
    }
    return payload


def get_invalid_payload():
    payload = {
        'id': 'some-fake-id',
        'author_id': 23,
        'name': 'cutting a wood',
        'description': 'learning how to cut firewood',
        'type': 'text',
        'text': 'first pick up some wood then ...',
        'created': '2012-12-31 23:59:59',
        'updated': '2012-12-31 23:59:59',
        'tags': ['tag-1', 'tag-2']
    }
    return payload


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


def test_create_chunk(chunk_dispose_list):
    url = CHUNK_APP + '/api/chunk'
    payload = get_valid_payload()
    chunk_dispose_list.append(copy.deepcopy(payload))
    r = requests.post(url, json=payload)
    assert r.status_code == 200
    chunk_id = r.json()['inserted_id']

    # check if the inserted chunk = payload
    url = CHUNK_APP + '/api/chunk/' + chunk_id
    r = requests.get(url)
    assert r.status_code == 200
    obj = payload
    obj['id'] = chunk_id
    assert obj == r.json()


def test_create_chunk_fail(chunk_dispose_list):
    url = CHUNK_APP + '/api/chunk'
    payload = get_invalid_payload()
    chunk_dispose_list.append(copy.deepcopy(payload))
    r = requests.post(url, json=payload)
    assert r.status_code == 400


def test_delete_chunk(chunk_ids):
    (cid, _) = chunk_ids[0]
    url = CHUNK_APP + '/api/chunk/' + cid
    r = requests.delete(url)
    assert r.status_code == 200

    # query check for the deleted chunk
    r = requests.get(url)
    assert r.status_code == 500


def test_delete_invalid_id():
    fake_id = 'some-fake-id'
    url = CHUNK_APP + '/api/chunk/' + fake_id
    r = requests.delete(url)
    assert r.status_code == 400


def test_delete_non_exist_chunk():
    valid_id = '123456789012345678901234'
    url = CHUNK_APP + '/api/chunk/' + valid_id
    r = requests.delete(url)
    assert r.status_code == 500
    assert r.text == 'no chunk found with id: {}'.format(valid_id)

#   TODO: write test for edit, search
