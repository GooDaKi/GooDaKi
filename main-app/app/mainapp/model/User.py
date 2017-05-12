import hashlib
import urllib

from flask import g
from passlib.hash import bcrypt_sha256

USER_EDITABLE = ['username', 'password', 'email' ,'first_name','last_name','sex','phone','address','birth_date']


class User:
    def __init__(self, db_row):
        self.user_id = None
        self.username = None
        self.password = None
        self.first_name = None
        self.last_name = None
        self.sex = None
        self.phone = None
        self.email = None
        # self.status = None
        self.birth_date = None
        self.address = None
        self.display_img_url = None
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True
        # self.is_admin = False

        if db_row is None:
            return

        if type(db_row) in [list, tuple]:
            self.user_id = db_row[0]
            self.username = db_row[1]
            self.display_name = db_row[2]
            self.email = db_row[3]
            # self.status = db_row[5]
        elif type(db_row) is dict:
            for key, val in db_row.items():
                setattr(self, key, val)

        # self.display_img_url = User.get_gravatar_url(self.email)
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        # self.is_admin = (self.status == 9999)

    def edit(self, options):
        if not all(map(lambda k: k in USER_EDITABLE, options.keys())):
            return None
        for key, val in options.items():
            setattr(self, key, val)
        if 'password' in options.keys():
            self.password = bcrypt_sha256.encrypt(self.password)
        return True

    def save(self):
        cursor = g.db.cursor()
        cursor.execute("""
            UPDATE "User" SET (username,firstname,lastname,email,phone,sex,address,birthdate) = (%s, %s,%s, %s,%s, %s,%s, %s) WHERE userid = (%s)
        """, [self.username,self.first_name,self.last_name,self.email,self.phone,self.address,self.birth_date,self.user_id])

        if cursor.rowcount < 0:
            cursor.close()
            return None

        if hasattr(self, 'password'):
            cursor.close()
            cursor = g.db.cursor()
            cursor.execute("""UPDATE "User" SET (password) = (%s) WHERE userid = (%s)""",
                           [self.password, self.user_id])
            if cursor.rowcount < 0:
                cursor.close()
                return None
            cursor.close()

        g.db.commit()
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
    def try_login(username, password):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "User" WHERE username = %s', (username,))
        if cursor.rowcount == 0:
            return None
        row = cursor.fetchone()
        hashed = row[4]
        cursor.close()
        if not bcrypt_sha256.verify(password, hashed):
            return -1
        u = User(row)
        # model_utils.add_system_log(u.user_id, 'signed in')
        return u

    @staticmethod
    def try_register(username,  password, email, firstname, lastname, sex, phone, birthdate, address):
        hashed_password = bcrypt_sha256.encrypt(password)
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "User" WHERE username = %s', (username,))
        if cursor.rowcount > 0:
            return -1  # username already exist
        cursor.execute('SELECT * FROM "User" WHERE email = %s', (email,))
        if cursor.rowcount > 0:
            return -2  # email already exist
        cursor.execute("""
            INSERT INTO "User" (username,  password, email, firstname, lastname, sex, phone, birthdate, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ) RETURNING userid""",
                       [username.lower(), hashed_password, email.lower(), firstname,lastname,sex,phone,birthdate,address])
        if cursor.rowcount == 0:
            return None  # TODO fix this (if cannot insert)
        g.db.commit()
        user_id = cursor.fetchone()[0]
        cursor.close()
        u = User.load(user_id)
        # model_utils.add_system_log(u.user_id, 'registered')
        return u
