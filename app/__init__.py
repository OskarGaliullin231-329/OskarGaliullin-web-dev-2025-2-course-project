# import os

from flask import Flask
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
    
    from .routing import note_view
    app.register_blueprint(note_view.bp)
    app.route('/', endpoint='index')(note_view.index)
    
    return app
