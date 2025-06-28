from flask import g, current_app
import mysql.connector
from mysql.connector import pooling

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
            'database': current_app.config['MYSQL_DATABASE'],
            'autocommit': True,
            'charset': 'utf8mb4',
            'use_unicode': True,
            'get_warnings': True,
            'raise_on_warnings': True,
            'connection_timeout': 60,
            'pool_name': 'mypool',
            'pool_size': 5
        }
        
    def connect(self):
        if 'db' not in g:
            try:
                g.db = mysql.connector.connect(**self._get_config())
            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    raise RuntimeError("Database access denied")
                elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                    raise RuntimeError("Database does not exist")
                else:
                    raise RuntimeError(f"Database error: {err}")
        return g.db
    
    def disconnect(self, e=None):
        if 'db' in g:
            try:
                g.db.close()
            except:
                pass
        g.pop('db', None)
