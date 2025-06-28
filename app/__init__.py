import os
from flask import Flask, session
from flask_session import Session

from .db_instance import db


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XNBzeuqo+zcYg4l9g17zLbKezSuONQikby7jvOVsnKhcixDlVGm0pCtCzqda6iel')
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', '127.0.0.1')
    app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_DATABASE', 'CP_test_db')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'CP_flask_app')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'qwerty')
    app.config['SESSION_PERMANENT'] = os.environ.get('SESSION_PERMANENT', 'False').lower() == 'true'
    app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE', 'filesystem')
    
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
