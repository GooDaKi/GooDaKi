import flask_login
import requests
from flask import request, session, flash, redirect, url_for, render_template, jsonify, abort, g
from flask_login import login_required, current_user
from wtforms import Form, StringField, validators, PasswordField, BooleanField, HiddenField
from passlib.hash import bcrypt_sha256
from mainapp import app, login_manager
from datetime import datetime
import mainapp.model as model

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=50)])
    password = StringField('Password', [validators.Length(min=3, max=255)])
    remember = BooleanField('Remember')

class RegisterForm(Form):
    username = StringField('Username', [validators.Regexp('^[a-zA-Z0-9_]+$', message="ชื่อผู้ใช้ต้องประกอบไปด้วยอักขระ a-z, 0-9 หรือ _ เท่านั้น"),validators.Length(min=3, max=50)])
    first_name = StringField('FirstName', [validators.Length(min=1, max=255, message='กรุณากรอกชื่อให้ถูกต้อง')])
    last_name = StringField('LastName', [validators.Length(min=1, max=255, message='กรุณากรอกนามสกุลให้ถูกต้อง')])
    birth_date = StringField('BirthDate')
    address = StringField('Address',
                          [validators.Length(min=5, message='กรุณากรอกที่อยู่ที่สามารถติดต่อได้อย่างละเอียด')])
    phone = StringField('Phone', [
        validators.Regexp('^[0-9]', message="กรุณากรอกเบอร์โทรศัพท์เป็นตัวเลขเท่านั้น"),
        validators.Length(min=9, max=10,
                          message='กรุณากรอกเบอร์โทรศัพท์ที่สามารถติดต่อได้ (ความยาว 9 หรือ 10 ตัวอักษร)')])
    sex = StringField('Sex', [validators.Length(min=1, max=1)])
    email = StringField('Email', [validators.Length(min=3, max=254), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.Length(min=6, max=50,
                                                            message='รหัสผ่านต้องมีความยาวอยู่ในช่วง 6 ถึง 50 ตัวอักษร'),
                                          validators.EqualTo('confirm_password', message='รหัสผ่านไม่ตรงกัน')])
    confirm_password = PasswordField('ConfirmPassword')


class EditAccountForm(RegisterForm):
    username = StringField('Username', [validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.Length(min=3, max=255)])
    confirm_password = None



class EditPasswordForm(Form):
    old_password = PasswordField('OldPassword', [validators.InputRequired(message='คุณจำเป็นต้องกรอกรหัสผ่านเดิมด้วย')])
    new_password = PasswordField('NewPassword', [validators.InputRequired(),
                                                 validators.Length(min=6, max=50,
                                                                   message='รหัสผ่านใหม่ต้องมีความยาวอยู่ในช่วง 6 ถึง 50 ตัวอักษร'),
                                                 validators.EqualTo('confirm_new_password',
                                                                    message='รหัสผ่านใหม่ไม่ตรงกัน กรุณาลองใหม่อีกครั้ง')])
    confirm_new_password = PasswordField('ConfirmNewPassword')

# User ########################################################################################

@login_manager.user_loader
def flask_load_user(userid):
    return model.User.load(userid)

# @app.route('/api/main/login', methods=["GET"])
# def render_login():
#     if flask_login.current_user.is_authenticated:
#         return redirect('/')
#     return render_template('login.html')


@app.route('/api/main/login', methods=["POST"])
def process_login():
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
            flask_login.login_user(u, remember=form.remember.data)
            return redirect("")
    return redirect(url_for('render_login'))

#
# @app.route('/api/main/register', methods=['GET'])
# def render_register():
#     return render_template('register_page.html')


@app.route('/main/register', methods=['POST'])
def process_register():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        sex = form.sex.data
        phone = form.phone.data
        birth_date = form.birth_date.data
        address = form.address.data
        user_out = model.User.try_register(username,  password, email, first_name, last_name, sex, phone, birth_date, address)

        if user_out == -1:
            # TODO handle when username already exist
            render_template('register_page.html', error='error-1')
        elif user_out == -2:
            # TODO handle when e-mail already exist
            render_template('register_page.html', error='error-2')
        else:
            # register successful
            return render_template('login.html', registered='successfully')
    # return render_template('register_page.html', error='error-0')
    return "register"


@app.route("/api/main/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/')


@app.route("/account/edit", methods=["POST"])
@flask_login.login_required
def edit_account():
    user = current_user
    form = EditAccountForm(request.form)
    if form.validate():
        sid = form.sid.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        sex = form.gender.data
        phone = form.tel.data
        birthdate = form.birth_date.data
        address = form.address.data
        allergies = form.allergies.data
        user_out = user.edit_account(sid, password, email, firstname, lastname, sex, phone, birthdate, address,
                                     allergies)
        if user_out == -1:
            flash("รหัสผ่านไม่ถูกต้อง", 'error')
            render_template('user_edit_account.html', form=form, user=user)
        elif user_out == -2:
            flash('อีเมลนี้ตรงกับผู้ใช้คนอื่น โปรดแก้ไข', 'error')
            render_template('user_edit_account.html', form=form, user=user)
        elif user_out == -3:
            flash('เลขประจำตัวประชนนี้ตรงกับผู้ใช้คนอื่น โปรดแก้ไข', 'error')
            render_template('user_edit_account.html', form=form, user=user)
        elif user_out is not None:
            # edit successful
            flash('บันทึกสำเร็จแล้ว', 'success')
            return redirect(url_for('show_edit_account'))
    # TODO: handle for each invalid field.
    errors = []
    for key in form.errors:
        errors.append(form.errors[key][0])
    return render_template('user_edit_account.html', form=form, error=errors, user=user)


#
# @app.route("/account/edit/password", methods=["POST"])
# @flask_login.login_required
# def edit_account_password():
#     user = current_user
#     form = EditPasswordForm(request.form)
#     if form.validate():
#         old_password = form.old_password.data
#         new_password = form.new_password.data
#         confirm_new_password = form.confirm_new_password.data
#         user_out = user.set_password(old_password, new_password)
#         if user_out is None:
#             flash("คุณกรอกรหัสผ่านเดิมไม่ถูกต้อง", 'error')
#         else:
#             flash('เปลี่ยนรหัสผ่านสำเร็จ', 'success')
#     else:
#         for key in form.errors:
#             for e in form.errors[key]:
#                 flash(e, 'error')
#     return redirect(url_for('show_edit_account'))