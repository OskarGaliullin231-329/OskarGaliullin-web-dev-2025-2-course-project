# import os

from flask import Flask, session
from flask_session import Session
from .db_instance import db


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    
    app.extensions['db'] = db
    
    from .cli import init_db_command
    app.cli.add_command(init_db_command)
    
    from .routing import auth
    app.register_blueprint(auth.bp)
    auth.login_manager.init_app(app)
    app.route('/', endpoint='login')(auth.login)
    
    from .routing import note_view
    app.register_blueprint(note_view.bp)
    
    Session(app)
    
    return app
