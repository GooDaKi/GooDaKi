#!/usr/bin/env python3

from chunkapp import app, mongo
from flask import g
from .chunk import Chunk
from bson.objectid import ObjectId

# from .user import User
# from .patient import Patient
# from .doctor import Doctor
# from .staff import Staff
# from .nurse import Nurse
# from .admin import Admin
# from .pharmacist import Pharmacist
# from .department import Department

@app.before_request
def before_request():
    g.db = db = mongo.db
    g.ObjectId = ObjectId


@app.teardown_request
def teardown_request(exception):
    pass
    # db = getattr(g, 'db', None)
    # if db is not None:
    # db.close()
