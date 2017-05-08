# #!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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
