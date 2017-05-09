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
def getAllCourse():
	cur_course_count = request.args.get('course-count', 0, type=int)
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		out,more_courses = model.Course.get_all(limit_no=limit,scroll_no=cur_course_count,all=False)
	else:
		out, more_courses = model.Course.get_all()
	return jsonify(dict(course=list(map(lambda x: x.__dict__, out)), more_courses=more_courses))


@app.route('/api/course/<id>', methods=['GET'])
def getCourseInfo(id):
	out = model.Course.get_by_id(id)
	return jsonify(out.__dict__)

@app.route('/api/course/author/<authorid>' , methods=['GET'])
def getCourseByAuthor(authorid):
	cur_course_count = request.args.get('course-count', 0, type=int)
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		out,more_courses = model.Course.get_by_author_id(authorid,limit_no=limit,scroll_no=cur_course_count,all=False)
	else:
		out,more_courses = model.Course.get_by_author_id(authorid)
	return jsonify(dict(course=list(map(lambda x: x.__dict__, out)), more_courses=more_courses))


# example request for create
# {
# 	"courseName":"testssssssssssssssssssssssssssss",
# 	"description":"testcreatecourse2",
# 	"authorID":1,
# 	"subjects":[1,3] <-- option
# }

@app.route('/api/course' , methods=['POST'])
def createCourse():
	info = request.get_json()
	out = model.Course.create(info)
	if out is None:
		return 'error occurred.', 400
	return 'successfully create course name: {}'.format(info['courseName'])

# example request for search
# {
# 	"query":1,
# 	"course-count":0 <- option
# }
@app.route('/api/course/search' , methods=['POST'])
def searchCourse():
	info = request.get_json()
	if 'course-count' in info:
		cur_course_count = info['course-count']
	else:
		cur_course_count = 0
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		out, more_courses = model.Course.search(info['query'], limit_no=limit, scroll_no=cur_course_count,all=False)
	else:
		out, more_courses = model.Course.search(info['query'])
	return jsonify(dict(course=list(map(lambda x: x.__dict__, out)), more_courses=more_courses))

# example request for edit
# {
# 	"courseID":1,
# 	"courseName":"testssssssssssssssssssssssssssss",
# 	"description":"testcreatecourse2",
# 	"subjects":[1,3]
#  all field is option except id
# }

@app.route('/api/course' , methods=['PUT'])
def editCourse():
	info = request.get_json()
	out = model.Course.get_by_id(info['courseID'])
	result = out.edit(info)
	if result is None:
		return 'error occurred.', 400
	return 'successfully edit course name: {}'.format(name)

@app.route('/api/course/<id>', methods=['DELETE'])
def deleteCourse(id):
	ret = model.Course.delete_by_id(id)
	if ret is None:
		return 'error occurred. Maybe the id is invalid', 400
	return 'deleted select with id: {}'.format(id)

# subject ################################################################

@app.route('/api/course/subject/<id>', methods=['GET'])
def getSubjectInfo(id):
	out = model.Subject.get_by_id(id)
	url_base = 'http://chunk-app:5000/api/chunk/'
	checked_chunk = list()
	for chunk in out.chunks:
		chunk_raw = requests.get(url_base + chunk[0]).json()
		if not 'error' in chunk_raw:
			checked_chunk.append(chunk[0])
	out.chunks = checked_chunk
	return jsonify(out.__dict__)

@app.route('/api/course/subject' , methods=['GET'])
def getAllSubject():
	cur_subject_count = request.args.get('subject-count', 6, type=int)
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		outs,more_subjects = model.Subject.get_all(limit_no=limit, scroll_no=cur_subject_count,all=False)
	else:
		outs,more_subjects = model.Subject.get_all()
	url_base = 'http://chunk-app:5000/api/chunk/'
	for out in outs:
		checked_chunk = list()
		for chunk in out.chunks:
			chunk_raw = requests.get(url_base + chunk[0]).json()
			if not 'error' in chunk_raw:
				checked_chunk.append(chunk[0])
		out.chunks = checked_chunk
	return jsonify(dict(course=list(map(lambda x: x.__dict__, outs)), more_subjects=more_subjects))

@app.route('/api/course/subject/author/<authorid>' , methods=['GET'])
def getSubjectByAuthor(authorid):
	cur_subject_count = request.args.get('subject-count', 0, type=int)
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		outs,more_subjects = model.Subject.get_by_author_id(authorid,limit_no=limit, scroll_no=cur_subject_count,all=False)
	else:
		outs,more_subjects = model.Subject.get_by_author_id(authorid)
	url_base = 'http://chunk-app:5000/api/chunk/'
	for out in outs:
		checked_chunk = list()
		for chunk in out.chunks:
			chunk_raw = requests.get(url_base + chunk[0]).json()
			if not 'error' in chunk_raw:
				checked_chunk.append(chunk[0])
		out.chunks = checked_chunk
	return jsonify(dict(course=list(map(lambda x: x.__dict__, outs)), more_subjects=more_subjects))

# example request for create
# {
# 	"subjectName":"testssss",
# 	"description":"testcreatesubject2",
# 	"authorID":1,
# 	"chunks":[] <-- option
# }

@app.route('/api/course/subject' , methods=['POST'])
def createSubject():
	info = request.get_json()
	out = model.Subject.create(info)
	if out is None:
		return 'error occurred.', 400
	return 'successfully create subject name: {}'.format(info['subjectName'])

# example request for search
# {
# 	"query":1,
# 	"subject-count":0 <- option
# }

@app.route('/api/course/subject/search' , methods=['POST'])
def searchSubject():
	info = request.get_json()
	if 'subject-count' in info:
		cur_subject_count = info['subject-count']
	else:
		cur_subject_count = 0
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		outs, more_subjects = model.Subject.search(info['query'], limit_no=limit, scroll_no=cur_subject_count,all=False)
	else:
		outs, more_subjects = model.Subject.search(info['query'])

	url_base = 'http://chunk-app:5000/api/chunk/'
	for out in outs:
		checked_chunk = list()
		for chunk in out.chunks:
			chunk_raw = requests.get(url_base + chunk[0]).json()
			if not 'error' in chunk_raw:
				checked_chunk.append(chunk[0])
		out.chunks = checked_chunk
	return jsonify(dict(course=list(map(lambda x: x.__dict__, outs)), more_subjects=more_subjects))

# example request for edit
# {
# 	"subjectID":1,
# 	"courseName":"testssssssssssssssssssssssssssss",
# 	"description":"testcreatecourse2",
# 	"chunks":[]
#  all field is option except id
# }

@app.route('/api/course/subject' , methods=['PUT'])
def editSubject():
	info = request.get_json()
	out = model.Subject.get_by_id(info['subjectID'])
	result = out.edit(info)
	if result is None:
		return 'error occurred.', 400
	return 'successfully edit subject name: {}'.format(info['subjectName'])

@app.route('/api/course/subject/<id>', methods=['DELETE'])
def deleteSubject(id):
	ret = model.Subject.delete_by_id(id)
	if ret is None:
		return 'error occurred. Maybe the id is invalid', 400
	return 'deleted select with id: {}'.format(id)


# career #####################################################################

@app.route('/api/course/career/<id>', methods=['GET'])
def getCareerInfo(id):
	out = "getcareerInfo"
	return out

@app.route('/api/course/career/author/<authorid>' , methods=['GET'])
def getCareerByAuthor(authorid):
	out = "getcareerInfobyauthor"
	return out

@app.route('/api/subject/career' , methods=['POST'])
def createCareer():
	info = request.get_json()
	out = "createcareer"
	return out

@app.route('/api/course/career/search' , methods=['POST'])
def searchCareer():
	info = request.get_json()
	out = "searchcareer"
	return out

@app.route('/api/course/career' , methods=['PUT'])
def editCareer():
	info = request.get_jso
	out = "editcareer"
	return out

@app.route('/api/course/career/<id>', methods=['DELETE'])
def deleteCareer(id):
	out = "deletecareer"
	return out