# #!/usr/bin/env python3

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)
app.config.from_object(__name__)
db = psycopg2.connect(host="main-db", database="goodaki", user="goodaki", password="goodaki")

# import mainapp.controller as controller
# import mainapp.model as model

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
