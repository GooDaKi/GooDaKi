# #!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(__name__)

app.config['MONGO_DBNAME'] = 'goodaki'
app.config['MONGO_HOST'] = 'chunk-db'
app.config['MONGO_PORT'] = '27017'

mongo = PyMongo(app)

import chunkapp.controller as controller
import chunkapp.model as model

@app.route('/')
def hello():
    return "Hello, This is GooDaKi chunk app"

@app.route('/api/demo')
def api_demo_get():
    return jsonify(dict(success=True))

@app.route('/api/demo_post', methods=["POST"])
def api_demo_post():
    json = request.get_json()
    return jsonify(json)
    
@app.route('/api/new/<name>')
def new_star(name):
    star = mongo.db.stars
    star_id = star.insert({'name': name, 'distance': 15})
    new_star = star.find_one({'_id': star_id })
    output = {'name' : new_star['name'], 'distance' : new_star['distance']}
    return jsonify({'result' : output})

@app.route('/api/test')
def foo():
    return 'hello world'

@app.route('/api/find')
def fuck():
    arr = list()
    for doc in mongo.db.stars.find({}):
        arr.append(dict(name=doc['name'], distance=doc['distance']))
    return jsonify(arr)

@app.route('/api/testnotfound')
def not_found():
    obj = mongo.db.stars.find({'name': 'haha you will not find me'})
    return jsonify(obj)
