from functools import wraps
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from app.repositories import UserRepository, NoteRepository, FileRepository
from app.db_instance import db
# from .user import User
import re

user_repo = UserRepository(db)
note_repo = NoteRepository(db)
file_repo = FileRepository(db)

bp = Blueprint('note_view', __name__, url_prefix='/note_view')

@bp.route('/')
# @login_required
# current_user.user_UUID
def index():
    notes = note_repo.get_all_notes_by_user_UUID('dddf59b4-48b3-11f0-bfde-44fa6636f0a3');
    print(notes)
    return render_template('note_view/index.html', notes_arr=notes)

# @bp.route('/<int:note_UUID>')
# @login_required
# def show_note(note_UUID):
#     notes = note_repo.get_all_notes_by_user_UUID(current_user.user_UUID);
#     return render_template('note_view/index.html', notes_arr=notes)
