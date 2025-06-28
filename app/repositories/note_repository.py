class NoteRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    def get_all_notes_by_user_UUID(self, user_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT note_name, note_UUID FROM notes WHERE user_UUID = %s;', (user_UUID, ))
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
    
    def get_note_by_UUID(self, note_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM notes WHERE note_UUID = %s;', (note_UUID, ))
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
    
    def create_note(self, note_name, note_text, user_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            query = '''
                        insert into notes (note_UUID, note_name, note_text, user_UUID) 
                        values
                        (UUID(), %s, %s, %s)
                    '''
            note_data = (note_name, note_text, user_UUID)
            cursor.execute(query, note_data)
            connection.commit()
            
            # Get the generated UUID - use a separate query to avoid cursor conflicts
            cursor.execute('SELECT note_UUID FROM notes WHERE note_name = %s AND user_UUID = %s ORDER BY note_UUID DESC LIMIT 1', (note_name, user_UUID))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            if cursor:
                cursor.close()
    
    def update_note(self, note_UUID, note_name, note_text):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            query = '''
                        update notes
                        set note_name = %s,
                            note_text = %s
                        where note_UUID = %s;
                    '''
            note_data = (note_name, note_text, note_UUID)
            cursor.execute(query, note_data)
            connection.commit()
        finally:
            if cursor:
                cursor.close()
    
    def delete_note(self, note_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            query = '''
                        delete from notes
                        where note_UUID = %s;
                    '''
            cursor.execute(query, (note_UUID, ))
            connection.commit()
        finally:
            if cursor:
                cursor.close()
