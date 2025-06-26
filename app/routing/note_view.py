from functools import wraps
from collections import namedtuple
from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from app.repositories import UserRepository, NoteRepository, FileRepository
from app.db_instance import db
from markdown import markdown
from bleach import clean

import re

user_repo = UserRepository(db)
note_repo = NoteRepository(db)
file_repo = FileRepository(db)

bp = Blueprint('note_view', __name__, url_prefix='/note_view')

# user_UUID = '9c4de172-4a4b-11f0-9092-44fa6636f0a3'
Note = namedtuple('Note', ['note_UUID', 'note_name', 'note_text', 'user_UUID'])

@bp.route('/<string:user_UUID>', methods=['GET', 'DELETE'])
@login_required
def index(user_UUID):
    notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
    return render_template('note_view/index.html', notes_arr=notes, user_id=user_UUID)

@bp.route('/<string:user_UUID>/<string:note_UUID>/view')
@login_required
def note_view(user_UUID, note_UUID):
    notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
    note = Note(*note_repo.get_note_by_UUID(note_UUID))
    return render_template(
        'note_view/note.html', 
        notes_arr=notes, 
        name=note.note_name, 
        text=clean(
            markdown(note.note_text),
            tags={'a', 'p', 'h1', 'h2', 'h3', 'h4', 'strong', 'em', 'code', 'img'}
            ),
        user_id=user_UUID,
        note_id=note_UUID
        )

@bp.route('/<string:user_UUID>/<string:note_UUID>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(user_UUID, note_UUID):
    notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
    Note = namedtuple('Note', ['note_UUID', 'note_name', 'note_text', 'user_UUID'])
    note = Note(*note_repo.get_note_by_UUID(note_UUID))
    
    if request.method == 'POST':
        note_name = request.form['note-name']
        note_text = request.form['note-text']
        note_repo.update_note(note_UUID, note_name, note_text)
        notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
        note = Note(*note_repo.get_note_by_UUID(note_UUID))
        return redirect(url_for('note_view.note_view', user_UUID=user_UUID, note_UUID=note_UUID))

    return render_template(
        'note_view/edit_note.html', 
        notes_arr=notes, 
        name=note.note_name, 
        text=note.note_text,
        user_id=user_UUID,
        note_id=note_UUID
        )

@bp.route('/<string:user_UUID>/new_note', methods=['GET', 'POST'])
@login_required
def new_note(user_UUID):
    if request.method == 'POST':
        note_name = request.form['note-name']
        note_text = request.form['note-text']
        note_repo.create_note(note_name, note_text, user_UUID)
        return redirect(url_for('note_view.index', user_UUID=user_UUID))
    notes = note_repo.get_all_notes_by_user_UUID(user_UUID)
    return render_template('note_view/new_note.html', notes_arr=notes, user_id=user_UUID)

@bp.route('/<string:user_UUID>/<string:note_UUID>/delete')
def delete_note(user_UUID, note_UUID):
    note_repo.delete_note(note_UUID)
    return redirect(url_for('note_view.index', user_UUID=user_UUID))
