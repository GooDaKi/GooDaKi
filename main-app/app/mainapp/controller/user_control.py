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
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        u = model.User.try_login(form.username.data, form.password.data)
        if u is None:
            # username does not exist
            flash('Unknown username', 'error')
            return redirect(url_for('render_login'))
        elif u == -1:
            flash('Wrong password', 'error')
            return redirect(url_for('render_login'))
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
            render_template('register.html', error='error-1')
        elif user_out == -2:
            # TODO handle when e-mail already exist
            render_template('register.html', error='error-2')
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

@flask_login.login_required
@app.route('/profile/<id>')
def render_profile(id):
    user=model.User.load(id)

    return render_template('profile.html',user=user)

@flask_login.login_required
@app.route('/search')
def render_search():
    return render_template('search.html',courses=None, subjects=None, chunks=None)

@flask_login.login_required
@app.route('/search', methods=['POST'])
def search_process():
    form = SearchForm(request.form)
    query = {
        'query': form.query.data
    }
    url_base = 'http://course-app:5000/api/course/'
    courses = requests.post(url_base+'search',json=query)
    try:
        courses = courses.json()
    except ValueError:
        courses = None
    careers = requests.post(url_base + 'career/search', json=query)
    try:
        careers = careers.json()
    except ValueError:
        careers = None
    subjects = requests.post(url_base+'subject/search',json=query)
    try:
        subjects = subjects.json()
    except ValueError:
        subjects = None

    url_base = 'http://chunk-app:5000/api/chunk/search'
    chunk_name = {
        'name': form.query.data
    }
    chunk_description = {
        'description': form.query.data
    }
    chunksA = requests.post(url_base,json=chunk_name)
    try:
        chunksA = chunksA.json()
    except ValueError:
        chunksA = []

    chunksB = requests.post(url_base, json=chunk_description)
    try:
        chunksB = chunksB.json()
    except ValueError:
        chunksB = []
    chunks = chunksA+chunksB
    if len(chunks)==0:
        chunks = None
    return render_template('search.html',careers=careers,courses=courses, subjects=subjects, chunks=chunks)

@flask_login.login_required
@app.route('/course/<id>')
def render_course(id):
    url_base = 'http://course-app:5000/api/course/'+id
    course = requests.get(url_base).json()
    subjects = list()
    for subject in course['subjects']:
        url_base = 'http://course-app:5000/api/course/subject/' + str(subject)
        subject = requests.get(url_base).json()
        new_chunks = list()
        for chunk in subject['chunks']:
            url_base = 'http://chunk-app:5000/api/chunk/' + chunk
            temp = requests.get(url_base).json()
            new_chunk = {
                'id': temp['id'],
                'name': temp['name'],
                'type':temp['type']
            }
            new_chunks.append(new_chunk)
        subject['chunks'] = new_chunks
        subjects.append(subject)

    return render_template('course.html', course=course, subjects=subjects)

@flask_login.login_required
@app.route('/subject/<id>')
def render_subject(id):
    url_base = 'http://course-app:5000/api/course/subject/'+id
    subject = requests.get(url_base).json()
    chunks = list()
    for chunk in subject['chunks']:
        url_base = 'http://chunk-app:5000/api/chunk/' + chunk
        chunks.append(requests.get(url_base).json())
    return render_template('subject.html', subject=subject, chunks=chunks)

@flask_login.login_required
@app.route('/career/<id>')
def render_career(id):
    url_base = 'http://course-app:5000/api/course/career/'+str(id)
    career = requests.get(url_base).json()
    courses = list()
    for course in career['courses']:
        url_base = 'http://course-app:5000/api/course/' + str(course)
        courses.append(requests.get(url_base).json())
    return render_template('career.html', career=career, courses=courses)

@flask_login.login_required
@app.route('/chunk/<type>/<id>')
def render_chunk(type,id):
    url_base = 'http://chunk-app:5000/api/chunk/' + id
    chunk_info = requests.get(url_base).json()
    if chunk_info is None:
        return None
    if type == 'video':
        return render_template('chunk_video.html',chunk=chunk_info)
    elif type == 'test':
        return render_template('chunk_test.html', chunk=chunk_info)
    else :
        return render_template('chunk_text.html', chunk=chunk_info)
