# #!/usr/bin/env python3
import flask_login
from flask import Flask, request, g, render_template, request, jsonify,redirect
import psycopg2


app = Flask(__name__, static_folder='../static', template_folder='../template')
app.config.from_object(__name__)
app.secret_key = "Goodaki"
db = psycopg2.connect(host="main-db", database="goodaki", user="goodaki", password="goodaki")
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import mainapp.controller as controller
import mainapp.model as model

@app.route('/')
def hello():
    user = flask_login.current_user
    if user.is_authenticated:
        g.user = user.get_id()
        return render_template('search.html', user=user)
    else:
        g.user = None
        return redirect('/register')


@app.route('/api/demo')
def api_demo_get():
    return jsonify(dict(success=True))


@app.route('/api/demo_post', methods=["POST"])
def api_demo_post():
    json = request.get_json()
    return jsonify(json)
