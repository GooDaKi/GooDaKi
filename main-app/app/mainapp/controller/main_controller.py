from courseapp import app
import courseapp.model as model
from operator import itemgetter
import json
import datetime
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import datetime

# course

@app.route('/api/course/<id>', methods=['GET'])
def getCourseInfo(id):
	out = "getcourseInfo"
    return out

@app.route('/api/course/author/<authorid>' , methods=['GET'])
def getCourseByAuthor(authorid):
	out = "getcourseInfobyauthor"
	return out

@app.route('/api/course' , methods=['POST'])
def createCourse():
	info = request.get_json()
	out = "createCourse"
	return out

@app.route('/api/course/search' , methods=['POST'])
def searchCourse():
	info = request.get_json()
	out = "searchCourse"
	return out

@app.route('/api/course' , methods=['PUT'])
def editCourse():
	info = request.get_jso
	out = "editCourse"
	return out

@app.route('/api/course/<id>', methods=['DELETE'])
def deleteCourse(id):
	out = "deleteCourse"
	return out

# subject

@app.route('/api/course/subject/<id>', methods=['GET'])
def getSubjectInfo(id):
	out = "getsubjectInfo"
    return out

@app.route('/api/course/subject/author/<authorid>' , methods=['GET'])
def getSubjectByAuthor(authorid):
	out = "getsubjectInfobyauthor"
	return out

@app.route('/api/course/subject' , methods=['POST'])
def createSubject():
	info = request.get_json()
	out = "createsubject"
	return out

@app.route('/api/course/subject/search' , methods=['POST'])
def searchSubject():
	info = request.get_json()
	out = "searchSubject"
	return out

@app.route('/api/course/subject' , methods=['PUT'])
def editSubject():
	info = request.get_jso
	out = "editSubject"
	return out

@app.route('/api/course/subject/<id>', methods=['DELETE'])
def deleteSubject(id):
	out = "deleteSubject"
	return out

# career

@app.route('/api/course/career/<id>', methods=['GET'])
def getSubjectInfo(id):
	out = "getcareerInfo"
    return out

@app.route('/api/course/career/author/<authorid>' , methods=['GET'])
def getSubjectByAuthor(authorid):
	out = "getcareerInfobyauthor"
	return out

@app.route('/api/course/career' , methods=['POST'])
def createSubject():
	info = request.get_json()
	out = "createcareer"
	return out

@app.route('/api/course/career/search' , methods=['POST'])
def searchSubject():
	info = request.get_json()
	out = "searchcareer"
	return out

@app.route('/api/course/career' , methods=['PUT'])
def editSubject():
	info = request.get_jso
	out = "editcareer"
	return out

@app.route('/api/course/career/<id>', methods=['DELETE'])
def deleteSubject(id):
	out = "deletecareer"
	return out

from courseapp import app
import courseapp.model as model
from operator import itemgetter
import json
import datetime
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import datetime

# course

@app.route('/api/course/<id>', methods=['GET'])
def getCourseInfo(id):
	out = "getcourseInfo"
    return out

@app.route('/api/course/author/<authorid>' , methods=['GET'])
def getCourseByAuthor(authorid):
	out = "getcourseInfobyauthor"
	return out

@app.route('/api/course' , methods=['POST'])
def createCourse():
	info = request.get_json()
	out = "createCourse"
	return out

@app.route('/api/course/search' , methods=['POST'])
def searchCourse():
	info = request.get_json()
	out = "searchCourse"
	return out

@app.route('/api/course' , methods=['PUT'])
def editCourse():
	info = request.get_jso
	out = "editCourse"
	return out

@app.route('/api/course/<id>', methods=['DELETE'])
def deleteCourse(id):
	out = "deleteCourse"
	return out

# subject

@app.route('/api/course/subject/<id>', methods=['GET'])
def getSubjectInfo(id):
	out = "getsubjectInfo"
    return out

@app.route('/api/course/subject/author/<authorid>' , methods=['GET'])
def getSubjectByAuthor(authorid):
	out = "getsubjectInfobyauthor"
	return out

@app.route('/api/course/subject' , methods=['POST'])
def createSubject():
	info = request.get_json()
	out = "createsubject"
	return out

@app.route('/api/course/subject/search' , methods=['POST'])
def searchSubject():
	info = request.get_json()
	out = "searchSubject"
	return out

@app.route('/api/course/subject' , methods=['PUT'])
def editSubject():
	info = request.get_jso
	out = "editSubject"
	return out

@app.route('/api/course/subject/<id>', methods=['DELETE'])
def deleteSubject(id):
	out = "deleteSubject"
	return out

# career

@app.route('/api/course/career/<id>', methods=['GET'])
def getSubjectInfo(id):
	out = "getcareerInfo"
    return out

@app.route('/api/course/career/author/<authorid>' , methods=['GET'])
def getSubjectByAuthor(authorid):
	out = "getcareerInfobyauthor"
	return out

@app.route('/api/course/career' , methods=['POST'])
def createSubject():
	info = request.get_json()
	out = "createcareer"
	return out

@app.route('/api/course/career/search' , methods=['POST'])
def searchSubject():
	info = request.get_json()
	out = "searchcareer"
	return out

@app.route('/api/course/career' , methods=['PUT'])
def editSubject():
	info = request.get_jso
	out = "editcareer"
	return out

@app.route('/api/course/career/<id>', methods=['DELETE'])
def deleteSubject(id):
	out = "deletecareer"
	return out

