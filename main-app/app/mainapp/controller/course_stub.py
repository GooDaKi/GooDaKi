from mainapp import app
import mainapp.model as model
from operator import itemgetter
import json
import datetime
import requests
from flask_login import login_required, current_user
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import datetime

# @app.route('/api/main/course',method=['POST'])
# def user_create_course():
#     info = request.get_json()
#     user = current_user.user_id
#     info['authorID'] = user
#     base_url = 'http://apt-app:5000/api/course'
#     res,id = requests.post(base_url, json=info)
#     if id != 400:
#         course = request.get(base_url+'/'+id)
#         return course
#     else:
#         return "error happens"
#
# @app.route('/api/main/course',method=['PUT'])
# def user_edit_course():
#     info = request.get_json()
#     user = current_user.user_id
#     base_url = 'http://apt-app:5000/api/course'
#     res, id = requests.put(base_url, json=info)
#     return jsonify(res)
#
# @app.route('/api/main/course/<course_id>',method=['GET'])
# def user_get_course(course_id):
#     info['authorID'] = user
#     base_url = 'http://apt-app:5000/api/course'
#     out = requests.get(base_url+'/'+course_id)
#     if out is None:
#         return 400
#     else:
#         return out





