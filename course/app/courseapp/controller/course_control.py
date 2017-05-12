from courseapp import app
import courseapp.model as model
from operator import itemgetter
import json
import datetime
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import datetime

# course

@app.route('/api/course/course/<id>', methods=['GET'])
def get_course_info(id):
    out = "getcourse_info"
    return out

@app.route('/api/course/course/author/<authorid>', methods=['GET'])
def get_course_by_author(authorid):
    out = "getcourse_infobyauthor"
    return out

@app.route('/api/course/course', methods=['POST'])
def create_course():
    info = request.get_json()
    out = "create_course"
    return out

@app.route('/api/course/course/search', methods=['POST'])
def search_course():
    info = request.get_json()
    out = "search_course"
    return out

@app.route('/api/course/course', methods=['PUT'])
def edit_course():
    info = request.get_jso
    out = "edit_course"
    return out

@app.route('/api/course/course/<id>', methods=['DELETE'])
def delete_course(id):
    out = "delete_course"
    return out

# subject

@app.route('/api/course/subject/<id>', methods=['GET'])
def get_subject_info(id):
    out = "getsubject_info"
    return out

@app.route('/api/course/subject/author/<authorid>', methods=['GET'])
def get_subject_by_author(authorid):
    out = "getsubject_infobyauthor"
    return out

@app.route('/api/course/subject', methods=['POST'])
def create_subject():
    info = request.get_json()
    out = "createsubject"
    return out

@app.route('/api/course/subject/search', methods=['POST'])
def search_subject():
    info = request.get_json()
    out = "search_subject"
    return out

@app.route('/api/course/subject', methods=['PUT'])
def edit_subject():
    info = request.get_jso
    out = "edit_subject"
    return out

@app.route('/api/course/subject/<id>', methods=['DELETE'])
def delete_subject(id):
    out = "delete_subject"
    return out

# career

@app.route('/api/course/career/<id>', methods=['GET'])
def get_career_info(id):
    out = "getcareer_info"
    return out

@app.route('/api/course/career/author/<authorid>', methods=['GET'])
def get_career_by_author(authorid):
    out = "getcareer_infobyauthor"
    return out

@app.route('/api/course/career', methods=['POST'])
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
