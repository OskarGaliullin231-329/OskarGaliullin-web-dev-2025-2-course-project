from functools import wraps
from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
# from collections import namedtuple
import mysql.connector as connector

from app.repositories import UserRepository
from app.db_instance import db
from .user import User
import re

user_repo = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйте для доступа к этому ресурсу'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_UUID):
    user = user_repo.get_by_UUID(user_UUID)
    if user:
        return User(user)
    return None

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['user_email']
        username = request.form['user_name']
        password = request.form['user_pass']
        remember_me = request.form.get('remember_me', None) == 'on'
        
        existing_user = user_repo.get_by_username_and_password(username, password)
        user_UUID = ''
        if existing_user:
            user_UUID = existing_user[0]
            flash('Registration failure. User already exists.', 'danger')
            return redirect(url_for('auth.register', user_UUID=user_UUID))
        
        existing_user = user_repo.get_by_username_and_password(user_email, password)
        user_UUID = ''
        if existing_user:
            user_UUID = existing_user[0]
            flash('Registration failure. User already exists.', 'danger')
            return redirect(url_for('auth.register', user_UUID=user_UUID))

        user_repo.create_user(username, password, user_email)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['user_pass']
        remember_me = request.form.get('remember_me', None) == 'on'
        
        user = user_repo.get_by_username_and_password(username, password)
        
        if user:
            flash('Authorization has gone successfully', 'success')
            login_user(User(user), remember=remember_me)
            session['user_UUID'] = user[0]
            return redirect(url_for('note_view.index', user_UUID=session['user_UUID']))
        
        flash('Authorization failure. Wrong username or password.', 'danger')
        
    return render_template('auth/login.html')

@bp.route('/account_details/<string:user_UUID>', methods=['GET', 'POST'])
@login_required
def account_details(user_UUID):
    user = user_repo.get_by_UUID(user_UUID)
    if request.method == 'POST':
        user_name = request.form['user-name']
        user_email = request.form['user-email']
        user_pass = request.form['user-pass']
        if not user_pass:
            user_repo.update_user_NE(user_UUID, user_name, user_email)
        user_repo.update_user(user_UUID, user_name, user_pass, user_email)
        # return redirect(url_for('note_view.index', user_UUID=user_UUID))
        print(request.form)

    return render_template(
        'auth/account_details.html',
        username=user[1],
        user_email=user[2],
        user_id = user_UUID
        )

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    redirect(url_for('auth.login'))
