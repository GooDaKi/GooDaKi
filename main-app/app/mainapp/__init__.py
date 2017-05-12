# #!/usr/bin/env python3

from flask import Flask, jsonify, request
import flask_login
import psycopg2

app = Flask(__name__)
app.config.from_object(__name__)
db = psycopg2.connect(host="main-db", database="goodaki", user="goodaki", password="goodaki")

<<<<<<< HEAD

# import mainapp.controller as controller
# import mainapp.model as model
=======
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import mainapp.controller as controller
import mainapp.model as model
>>>>>>> origin/orakanya_course_and_subject_service

@app.route('/')
def hello():
    return "Hello, This is GooDaKi main app"


@app.route('/api/demo')
def api_demo_get():
    return jsonify(dict(success=True))


@app.route('/api/demo_post', methods=["POST"])
def api_demo_post():
    json = request.get_json()
    return jsonify(json)

# @app.route('/')
# def main():
#     user = flask_login.current_user
#     if user.is_authenticated:
#         g.user = user.get_id()
#         return render_template('main.html', user=user)
#     else:
#         g.user = None
#         return render_template('landing.html')