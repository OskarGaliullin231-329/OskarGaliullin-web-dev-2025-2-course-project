from functools import wraps
from collections import namedtuple
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from app.repositories import UserRepository, NoteRepository, FileRepository
from app.db_instance import db
from markdown import markdown

import re

user_repo = UserRepository(db)
note_repo = NoteRepository(db)
file_repo = FileRepository(db)

bp = Blueprint('note_view', __name__, url_prefix='/note_view')

# user_UUID = '9c4de172-4a4b-11f0-9092-44fa6636f0a3'

@bp.route('/<string:user_UUID>')
@login_required
def index(user_UUID):
    notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
    print(notes)
    return render_template('note_view/index.html', notes_arr=notes)

@bp.route('/<string:user_UUID>/<string:note_UUID>/view')
@login_required
def note_view(user_UUID, note_UUID):
    notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
    Note = namedtuple('Note', ['note_UUID', 'note_name', 'note_text', 'user_UUID'])
    print(note_repo.get_note_by_UUID(note_UUID))
    note = Note(*note_repo.get_note_by_UUID(note_UUID))
    return render_template('note_view/note.html', notes_arr = notes, name=note.note_name, text=markdown(note.note_text))

