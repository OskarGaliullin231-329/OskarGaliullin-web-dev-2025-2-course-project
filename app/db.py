from flask import g, current_app
import mysql.connector

class DBConnector:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.teardown_appcontext(self.disconnect)
    
    def _get_config(self):
        if not self.app:
            raise RuntimeError('Application is not initialized')
        return {
            'user': current_app.config['MYSQL_USER'],
            'host': current_app.config['MYSQL_HOST'],
            'password': current_app.config['MYSQL_PASSWORD'],
            'database': current_app.config['MYSQL_DATABASE']
        }
        
    def connect(self):
        if 'db' not in g:
            g.db = mysql.connector.connect(**self._get_config())
        return g.db
    
    def disconnect(self, e=None):
        if 'db' in g:
            g.db.close()
        g.pop('db', None)
