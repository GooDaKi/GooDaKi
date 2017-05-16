#!/usr/bin/env python3

import flask_login
import requests
from flask import request, session, flash, redirect, url_for, render_template, jsonify, abort, g
from flask_login import login_required, current_user
from wtforms import Form, StringField, validators, PasswordField, BooleanField, HiddenField
from passlib.hash import bcrypt_sha256
from mainapp import app, login_manager
from datetime import datetime
import mainapp.model as model
import json

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=50)])
    password = StringField('Password', [validators.Length(min=3, max=255)])
    remember = BooleanField('Remember')


class RegisterForm(Form):
    username = StringField('Username', [
        validators.Length(min=3, max=50, message="username may be longer than 50 or shorter that 3")])
    displayname = StringField('Displayname', [
        validators.Length(min=3, max=50, message="displayname may be longer than 50 or shorter that 3")])
    email = StringField('Email',
                        [validators.Length(min=3, max=254), validators.Email(message="email is not validated")])
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.Length(min=6, max=50,
                                                            message="password may be longer than 50 or shorter that 6"),
                                          validators.EqualTo('confirm_password', message="password is not match")])
    confirm_password = PasswordField('ConfirmPassword')
    first_name = StringField('FirstName', [
        validators.Length(min=3, max=50, message="firstname may be longer than 50 or shorter that 3")])
    last_name = StringField('LastName', [
        validators.Length(min=3, max=50, message="lastname may be longer than 50 or shorter that 3")])


class SearchForm(Form):
    query = StringField('Query')

@login_manager.user_loader
def load_user(userid):
    user = model.User.load(userid)
    if user is None:
        return None
    # TODO implement some roles to authorize access
    return user


@app.route('/login', methods=["GET"])
def render_login():
    if flask_login.current_user.is_authenticated:
        return redirect('/')
    return render_template('login.html',error = None)


@app.route('/login', methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        u = model.User.try_login(form.username.data, form.password.data)
        if u is None:
            # username does not exist
            flash('Unknown username', 'error')
            return render_template('login.html',error='Unknown username')
        elif u == -1:
            flash('Wrong password', 'error')
            return render_template('login.html',error='Wrong password')
        else:
            # Login successful
            flask_login.login_user(u)
            return redirect("")
    return redirect(url_for('render_login'))


@app.route('/register', methods=['GET'])
def render_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_register():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        displayname = form.displayname.data
        email = form.email.data
        password = form.password.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        options = {
            'username': username,
            'displayname': displayname,
            'email': email,
            'password': password,
            'firstname': firstname,
            'lastname': lastname
        }
        user_out = model.User.try_register(options)
        if user_out == -1:
            # TODO handle when username already exist
            render_template('register.html', error='username already exist')
        elif user_out == -2:
            # TODO handle when e-mail already exist
            render_template('register.html', error='e-mail already exist')
        else:
            # register successful
            return render_template('login.html', registered='successfully')
    return render_template('register.html', error=form.errors)


# @app.route('/api/main/profile/<id>', methods=['GET'])
@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("")

########################################## SHOW taken course AND in-progress course ########################################

@flask_login.login_required
@app.route('/profile/<id>')
def render_profile(id):
    user = model.User.load(id)
    return render_template('profile.html', user=user)


############################################################################################################################