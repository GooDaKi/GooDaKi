#!/usr/bin/env python3

import flask_login
import requests
from flask import request, session, flash, redirect, url_for, render_template
from flask_login import login_required, current_user, login_manager
from wtforms import Form
from passlib.hash import bcrypt_sha256
from datetime import datetime
import mainapp.model as model


@login_manager.user_loader
def load_user(userid):
    user = model.User.load(userid)
    if user is None:
        return None
    # TODO implement some roles to authorize access
    return user


