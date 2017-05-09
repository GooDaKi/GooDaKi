from .course import Course
from .subject import Subject
# from .career import Career

from courseapp import app
from flask import g
import psycopg2

@app.before_request
def before_request():
    g.db = db = psycopg2.connect(host="course-db", database="goodaki", user="goodaki", password="goodaki")


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()