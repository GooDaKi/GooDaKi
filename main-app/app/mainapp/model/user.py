#!/usr/bin/env python3

from flask import g
from passlib.hash import bcrypt_sha256
import flask_login


class User:
    def __init__(self, options=None):
        if options is not None:
            options['id'] = options['userid']
            for key, val in options.items():
                setattr(self, key, val)
            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False
        else:
            self.id = None
            self.username = None
            self.displayname = None
            self.email = None
            self.firstname = None
            self.lastname = None
            self.is_active = False
            self.is_authenticated = False
            self.is_anonymous = True

    def get_id(self):
        return str(self.id)

    def get_fullname(self):
        return self.firstname + ' ' + self.lastname

    def verify_password(self, password):
        cursor = g.db.cursor()
        cursor.execute('select "password" from "User" where userID= (%s)', (self.user_id,))
        pwd = cursor.fetchone()['password']
        cursor.close()
        if not bcrypt_sha256.verify(password, pwd):
            return False
        return True

    def authenticate(self, password, remember=None):
        if not self.verify_password(password):
            return False
        flask_login.login_user(self, remember=remember)
        return True

    @staticmethod
    def load(user_id):
        user_id = int(user_id)
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "User" WHERE userID = %s', (user_id,))
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            cursor.close()
            return User(row)
        else:
            cursor.close()
            return None


    @staticmethod
    def load_by_username(username):
        cursor = g.db.cursor()
        cursor.execute('select * from "User" where username = (%s)', (username,))
        if cursor.rowcount != 1:
            cursor.close()
            return None
        obj = cursor.fetchone()
        cursor.close()
        return User(obj)

    @staticmethod
    def try_register(options):
        try:
            username = options.pop('username')
            displayname = options.pop('displayname')
            email = options.pop('email')
            firstname = options.pop('firstname')
            lastname = options.pop('lastname')
            password = options.pop('password')
            hashed_password = bcrypt_sha256.encrypt(password)
        except KeyError:
            # if options doesn't have needed keys
            return None

        cursor = g.db.cursor()
        check_valid = 0
        # check for username, email
        cursor.execute('select * from "User" where username=(%s)', (username,))
        if cursor.rowcount > 0:
            check_valid |= 1  # username already exists
        cursor.execute('select * from "User" where email=(%s)', (email,))
        if cursor.rowcount > 0:
            check_valid |= 2  # email already exists
        if check_valid != 0:
            return check_valid

        cursor.execute('''
            insert  into "User" (username, displayname, email, firstname, lastname, password) 
                    values (%s, %s, %s, %s, %s, %s) returning userid
        ''', (username, displayname, email, firstname, lastname, hashed_password))

        if cursor.rowcount == 0:
            # TODO error cannot insert using more elegant solutions?
            cursor.close()
            return None

        userid = cursor.fetchone()['userid']
        g.db.commit()
        cursor.close()
        user = User.load(userid)
        return user


    @staticmethod
    def try_login(username, password):
        # NOTE this is kinda different from class diagram where 'authenticate'
        # is not static. I've fix that. see authenticate() below. -- tae
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "User" WHERE username = %s', (username,))
        if cursor.rowcount == 0:
            return None
        row = cursor.fetchone()
        real_password = row['password']
        cursor.close()

        # TODO: bcrypt
        # if not bcrypt_sha256.verify(password, hashed):
        if not bcrypt_sha256.verify(password, real_password):
            return -1
        u = User(row)
        return u

    def get_take_course(self):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Take_Career" WHERE userID = %s', (self.id,))
        if cursor.rowcount == 0:
            return None
        careers = cursor.fetchall()
        cursor.close()
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Take_Course" WHERE userID = %s', (self.id,))
        if cursor.rowcount == 0:
            return None
        courses = cursor.fetchall()
        cursor.close()
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Take_Subject" WHERE userID = %s', (self.id,))
        if cursor.rowcount == 0:
            return None
        subjects = cursor.fetchall()
        cursor.close()
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Take_Chunk" WHERE userID = %s', (self.id,))
        if cursor.rowcount == 0:
            return None
        chunks = cursor.fetchall()
        cursor.close()
        return careers, courses, subjects, chunks


