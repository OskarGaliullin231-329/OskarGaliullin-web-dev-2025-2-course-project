from functools import wraps
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
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
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    redirect(url_for('login'))
