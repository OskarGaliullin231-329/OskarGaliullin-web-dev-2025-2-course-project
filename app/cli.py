import click
from flask import current_app
from flask.cli import with_appcontext
from .db_instance import db

@click.command('init-db')
@with_appcontext
def init_db_command():
    with current_app.open_resource('create_schema.sql') as f:
        sql_script = f.read().decode('utf8')

        connection = db.connect()
        cursor = connection.cursor()
        
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        cursor.close()
        click.echo('Initialized the database.')
