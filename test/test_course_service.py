#!/usr/bin/env python
import requests
import json
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
# define constants
COURSE_APP = 'http://localhost:5001'


def test_get_by_id():
    r = requests.get(COURSE_APP + '/api/course/1')
    assert r.status_code == 200
    print('test get_by_id: passed')


def test_get_by_id_fail():
    r = requests.get(COURSE_APP + '/api/course/10000')
    assert  r.status_code == 500
    print('test get_by_id_fail: passed')


def test_get_by_author():
    r = requests.get(COURSE_APP + '/api/course/author/1')
    assert r.status_code == 200
    print('test get_by_author: passed')


def test_get_by_author_fail():
    r = requests.get(COURSE_APP + '/api/course/author/10000')
    assert r.status_code == 500
    print('test get_by_author_fail: passed')


def test_create():
    json = {
        "courseName": "fromtest",
        "description": "fromtest",
        "authorID": 1
    }
    r = requests.post(COURSE_APP+'/api/course', json=json)
    assert r.status_code == 200
    print('test get_by_author: passed')


def test_edit():
    json = {
        "courseID": 2,
        "courseName": "fromtest",
        "description": "fromtest",
        "authorID": 1
    }
    r = requests.put(COURSE_APP+'/api/course', json=json)
    assert r.status_code == 200
    print('test edit: passed')


def test_edit_fail():
    json = {
        "courseID": 10000000,
        "courseName": "fromtest",
        "description": "fromtest",
        "authorID": 1
    }
    r = requests.put(COURSE_APP+'/api/course', json=json)
    assert r.status_code == 500
    print('test edit_fail: passed')


def test_search():
    info = {
        "query": "from"
    }
    r = requests.post(COURSE_APP+'/api/course/search',json=info)
    assert r.status_code == 200
    print('test search: passed')


def test_search_fail():
    info = {
        "query": "5555555555555555555555555555555555555555"
    }
    r = requests.post(COURSE_APP+'/api/course/search',json=info)
    assert r.status_code == 500
    print('test search_fail: passed')


def test_subject_get_by_id():
    r = requests.get(COURSE_APP + '/api/course/subject/1')
    assert r.status_code == 200
    print('test get_by_id: passed')


def test_subject_get_by_id_fail():
    r = requests.get(COURSE_APP + '/api/course/subject/10000')
    assert  r.status_code == 500
    print('test get_by_id_fail: passed')


def test_subject_get_by_author():
    r = requests.get(COURSE_APP + '/api/course/subject/author/1')
    assert r.status_code == 200
    print('test get_by_author: passed')


def test_subject_get_by_author_fail():
    r = requests.get(COURSE_APP + '/api/course/subject/author/10000')
    assert r.status_code == 500
    print('test get_by_author_fail: passed')


def test_subject_create():
    json = {
        "subjectName": "fromtest",
        "description": "fromtest",
        "authorID": 1
    }
    r = requests.post(COURSE_APP+'/api/course/subject', json=json)
    assert r.status_code == 200
    print('test get_by_author: passed')


def test_subject_edit():
    json = {
        "subjectID": 2,
        "subjectName": "fromtest",
        "description": "fromtest",
        "authorID": 1
    }
    r = requests.put(COURSE_APP+'/api/course/subject', json=json)
    assert r.status_code == 200
    print('test edit: passed')


def test_subject_edit_fail():
    json = {
        "subjectID": 10000000,
        "subjectName": "fromtest",
        "description": "fromtest",
        "authorID": 1
    }
    r = requests.put(COURSE_APP+'/api/course/subject', json=json)
    assert r.status_code == 500
    print('test edit_fail: passed')


def test_subject_search():
    info = {
        "query": "from"
    }
    r = requests.post(COURSE_APP+'/api/course/subject/search',json=info)
    assert r.status_code == 200
    print('test search: passed')


def test_subject_search_fail():
    info = {
        "query": "5555555555555555555555555555555555555555"
    }
    r = requests.post(COURSE_APP+'/api/course/subject/search',json=info)
    assert r.status_code == 500
    print('test search_fail: passed')
