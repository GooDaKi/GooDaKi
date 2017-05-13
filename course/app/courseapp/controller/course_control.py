from courseapp import app
import courseapp.model as model
from operator import itemgetter
import json
import datetime
import requests
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import datetime


# course ###############################################################
@app.route('/api/course', methods=['GET'])
def get_all_course():
    cur_course_count = request.args.get('course-count', 0, type=int)
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        courses, is_more_courses = model.Course.get_all(limit_no=limit, scroll_no=cur_course_count, all=False)
    else:
        courses, is_more_courses = model.Course.get_all()
        if courses is None or is_more_courses is None:
            return "None"
    return jsonify(dict(courses=list(map(lambda x: x.__dict__, courses)), is_more_courses=is_more_courses))


@app.route('/api/course/<id>', methods=['GET'])
def get_course_info(id):
    courses = model.Course.get_by_id(id)
    if courses is None:
        return None
    return jsonify(courses.__dict__)


@app.route('/api/course/author/<authorid>', methods=['GET'])
def get_course_by_author(authorid):
    cur_course_count = request.args.get('course-count', 0, type=int)
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        courses, is_more_courses = model.Course.get_by_author_id(authorid, limit_no=limit, scroll_no=cur_course_count,
                                                          all=False)
    else:
        courses, is_more_courses = model.Course.get_by_author_id(authorid)
        if courses is None or is_more_courses is None:
            return None
    return jsonify(dict(courses=list(map(lambda x: x.__dict__, courses)), is_more_courses=is_more_courses))


# example request for create
# {
# 	"courseName":"testssssssssssssssssssssssssssss",
# 	"description":"testcreatecourse2",
# 	"authorID":1,
# 	"subjects":[1,3] <-- option
# }

@app.route('/api/course', methods=['POST'])
def create_course():
    info = request.get_json()
    result = model.Course.create(info)
    if result is None:
        return None
    # return 'successfully create course name: {}'.format(info['courseName']), out
    return jsonify(result)


# example request for search
# {
# 	"query":1,
# 	"course-count":0 <- option
# }
@app.route('/api/course/search', methods=['POST'])
def search_course():
    info = request.get_json()
    if 'course-count' in info:
        cur_course_count = info['course-count']
    else:
        cur_course_count = 0
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        courses, is_more_courses = model.Course.search(info['query'], limit_no=limit, scroll_no=cur_course_count, all=False)
    else:
        courses, is_more_courses = model.Course.search(info['query'])
        if courses is None or is_more_courses is None:
            return None

    return jsonify(dict(course=list(map(lambda x: x.__dict__, courses)), is_more_courses=is_more_courses))


# example request for edit
# {
# 	"courseID":1,
# 	"courseName":"testssssssssssssssssssssssssssss",
# 	"description":"testcreatecourse2",
# 	"subjects":[1,3]
#  all field is option except id
# }

@app.route('/api/course', methods=['PUT'])
def edit_course():
    info = request.get_json()
    course = model.Course.get_by_id(info['courseID'])
    course = course.edit(info)
    result = course.save()
    if result is None:
        return None
    # return 'successfully edit course name: {}'.format(course.courseName), result
    return jsonify(result)


@app.route('/api/course/<id>', methods=['DELETE'])
def delete_course(id):
    ret = model.Course.delete_by_id(id)
    if ret is None:
        return 'error occurred. Maybe the id is invalid', 400
    return 'deleted select with id: {}'.format(id)


# subject ################################################################

@app.route('/api/course/subject/<id>', methods=['GET'])
def get_subject_info(id):
    subject = model.Subject.get_by_id(id)
    if subject is None:
        return None
    url_base = 'http://chunk-app:5000/api/chunk/'
    checked_chunk = list()
    for chunk in subject.chunks:
        chunk_raw = requests.get(url_base + chunk['chunkid']).json()
        if 'error' not in chunk_raw:
            checked_chunk.append(chunk['chunkid'])
    subject.chunks = checked_chunk
    return jsonify(subject.__dict__)


@app.route('/api/course/subject', methods=['GET'])
def get_all_subject():
    cur_subject_count = request.args.get('subject-count', 6, type=int)
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        subjects, is_more_subjects = model.Subject.get_all(limit_no=limit, scroll_no=cur_subject_count, all=False)
    else:
        subjects, is_more_subjects = model.Subject.get_all()
        if subjects is None:
            return None
    url_base = 'http://chunk-app:5000/api/chunk/'
    for subject in subjects:
        checked_chunk = list()
        for chunk in subject.chunks:
            chunk_raw = requests.get(url_base + chunk['chunkid']).json()
            if 'error' not in chunk_raw:
                checked_chunk.append(chunk['chunkid'])
        subject.chunks = checked_chunk
    return jsonify(dict(subjects=list(map(lambda x: x.__dict__, subjects)), is_more_subjects=is_more_subjects))


@app.route('/api/course/subject/author/<authorid>', methods=['GET'])
def get_subject_by_author(authorid):
    cur_subject_count = request.args.get('subject-count', 0, type=int)
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        subjects, is_more_subjects = model.Subject.get_by_author_id(authorid, limit_no=limit, scroll_no=cur_subject_count,
                                                             all=False)
    else:
        subjects, is_more_subjects = model.Subject.get_by_author_id(authorid)
        if subjects is None:
            return None
    url_base = 'http://chunk-app:5000/api/chunk/'
    for subject in subjects:
        checked_chunk = list()
        for chunk in subject.chunks:
            chunk_raw = requests.get(url_base + chunk['chunkid']).json()
            if 'error' not in chunk_raw:
                checked_chunk.append(chunk['chunkid'])
        subject.chunks = checked_chunk
    return jsonify(dict(subjects=list(map(lambda x: x.__dict__, subjects)), is_more_subjects=is_more_subjects))


# example request for create
# {
# 	"subjectName":"testssss",
# 	"description":"testcreatesubject2",
# 	"authorID":1,
# 	"chunks":[] <-- option
# }

@app.route('/api/course/subject', methods=['POST'])
def create_subject():
    info = request.get_json()
    result = model.Subject.create(info)
    if result is None:
        return None
    # return 'successfully create subject name: {}'.format(info['subjectName'])
    return jsonify(result)


# example request for search
# {
# 	"query":1,
# 	"subject-count":0 <- option
# }

@app.route('/api/course/subject/search', methods=['POST'])
def search_subject():
    info = request.get_json()
    if 'subject-count' in info:
        cur_subject_count = info['subject-count']
    else:
        cur_subject_count = 0
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        subjects, is_more_subjects = model.Subject.search(info['query'], limit_no=limit, scroll_no=cur_subject_count,
                                                   all=False)
    else:
        subjects, is_more_subjects = model.Subject.search(info['query'])
        if is_more_subjects is None:
            return None

    url_base = 'http://chunk-app:5000/api/chunk/'
    for subject in subjects:
        checked_chunk = list()
        for chunk in subject.chunks:
            chunk_raw = requests.get(url_base + chunk['chunkid']).json()
            if 'error' not in chunk_raw:
                checked_chunk.append(chunk['chunkid'])
        subject.chunks = checked_chunk
    return jsonify(dict(subjects=list(map(lambda x: x.__dict__, subjects)), is_more_subjects=is_more_subjects))


# example request for edit
# {
# 	"subjectID":1,
# 	"courseName":"testssssssssssssssssssssssssssss",
# 	"description":"testcreatecourse2",
# 	"chunks":[]
#  all field is option except id
# }

@app.route('/api/course/subject', methods=['PUT'])
def edit_subject():
    info = request.get_json()
    subject = model.Subject.get_by_id(info['subjectID'])
    subject = subject.edit(info)
    result = subject.save()
    if result is None:
        return None
    # return 'successfully edit subject name: {}'.format(info['subjectName'])
    return jsonify(result)


@app.route('/api/course/subject/<id>', methods=['DELETE'])
def delete_subject(id):
    ret = model.Subject.delete_by_id(id)
    if ret is None:
        return 'error occurred. Maybe the id is invalid', 400
    return 'deleted select with id: {}'.format(id)


# career #####################################################################

@app.route('/api/course/career/<id>', methods=['GET'])
def get_career_info(id):
    out = "getcareerInfo"
    return out


@app.route('/api/course/career/author/<authorid>', methods=['GET'])
def get_career_by_author(authorid):
    out = "getcareerInfobyauthor"
    return out


@app.route('/api/subject/career', methods=['POST'])
def create_career():
    info = request.get_json()
    out = "createcareer"
    return out


@app.route('/api/course/career/search', methods=['POST'])
def search_career():
    info = request.get_json()
    out = "searchcareer"
    return out


@app.route('/api/course/career', methods=['PUT'])
def edit_career():
    info = request.get_jso
    out = "editcareer"
    return out


@app.route('/api/course/career/<id>', methods=['DELETE'])
def delete_career(id):
    out = "deletecareer"
    return out

