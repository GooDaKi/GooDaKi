#!/usr/bin/env python3

from flask import g
from passlib.hash import bcrypt_sha256
import flask_login


class User:
    def __init__(self, options=None):
        if options is not None and type(options) is dict:
            options['id'] = options.pop('userID', None)
            options.pop('password')
            for key, val in options.items():
                setattr(self, key, val)
        else:
            self.id = None
            self.username = None
            self.displayname = None
            self.email = None
            self.firstname = None
            self.lastname = None

    def get_id(self):
        return str(self.id)

    def get_fullname(self):
        return self.firstname + ' ' + self.lastname

    def verify_password(self, password):
        cursor = g.db.cursor()
        cursor.execute('select "password" from "User" where userid= (%s)', (self.user_id,))
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
        if user_id is None:
            return None
        user_id = int(user_id)
        cursor = g.db.cursor('select * from "User" where userid = %s', (user_id,))
        if cursor.rowcount != 1:
            cursor.close()
            return None
        obj = cursor.fetchone()
        cursor.close()
        return User(obj)

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
