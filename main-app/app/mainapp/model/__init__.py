<<<<<<< HEAD
#!/usr/bin/env python3

# from .user import User
=======
from .User import User
# from .Portfolio import Portfolio
# from .career import Career
>>>>>>> origin/orakanya_course_and_subject_service

from mainapp import app
from flask import g
import psycopg2
<<<<<<< HEAD
import psycopg2.extras


@app.before_request
def before_request():
    g.db = db = psycopg2.connect(host="main-db", database="goodaki", user="goodaki", password="goodaki",
                                 cursor_factory=psycopg2.extras.RealDictCursor)
    register_new_date()
    register_new_decimal()
=======

@app.before_request
def before_request():
    g.db = db = psycopg2.connect(host="main-db", database="goodaki", user="goodaki", password="goodaki")
>>>>>>> origin/orakanya_course_and_subject_service


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
<<<<<<< HEAD
        db.close()


def register_new_date():
    # Cast PostgreSQL Date as Python string
    # Reference:
    # 1. http://initd.org/psycopg/docs/extensions.html#psycopg2.extensions.new_type
    # 2. http://initd.org/psycopg/docs/advanced.html#type-casting-from-sql-to-python
    # 1082 is OID for DATE type.
    new_date = psycopg2.extensions.new_type(psycopg2.extensions.DATE.values, 'DATE', psycopg2.STRING)
    psycopg2.extensions.register_type(new_date)


def register_new_decimal():
    new_decimal = psycopg2.extensions.new_type(psycopg2.extensions.DECIMAL.values, 'DECIMAL(4,2)', psycopg2.STRING)
    psycopg2.extensions.register_type(new_decimal)
=======
        db.close()
>>>>>>> origin/orakanya_course_and_subject_service
