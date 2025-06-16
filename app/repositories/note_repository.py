class NoteRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    def get_all_notes_by_user_UUID(self, user_UUID):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('SELECT note_name FROM notes WHERE user_UUID = %s;', (user_UUID, ))
            return cursor.fetchall()
    
    def get_note_by_UUID(self, note_UUID):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('SELECT * FROM notes WHERE note_UUID = %s;', (note_UUID, ))
            return cursor.fetchone()
    
    def create_note(self, note_name, note_text, user_UUID):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                    insert into notes (note_UUID, note_name, note_text, user_UUID) 
                    values
                    (UUID(), %s, %s, %s)
                    '''
            note_data = (note_name, note_text, user_UUID)
            cursor.execute(query, note_data)
            connection.commit()
            
    
    def update_note(self, note_UUID, note_name, note_text):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                    update notes
                    set note_name = %s,
                        note_text = %s,
                    where note_UUID = %s;
                    '''
            note_data = (note_name, note_text, note_UUID)
            cursor.execute(query, note_data)
            connection.commit()
    
    def delete_note(self, note_UUID):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                    delete from notes
                    where note_UUID = %s;
                    '''
            cursor.execute(query, note_UUID)
            connection.commit()
