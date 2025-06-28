class FileRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_all_filenames_by_note_UUID(self, note_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT file_name FROM note_files WHERE note_UUID = %s;', (note_UUID,))
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def get_all_files_by_note_UUID(self, note_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT file_name FROM note_files WHERE note_UUID = %s;', (note_UUID,))
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def add_file(self, file_name, note_UUID):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute('''
                           insert into note_files (file_name, note_UUID)
                           values (%s, %s);
                           ''', (file_name, note_UUID))
            connection.commit()
        finally:
            if cursor:
                cursor.close()

    def delete_file(self, note_UUID, file_name):
        connection = self.db_connector.connect()
        cursor = None
        try:
            cursor = connection.cursor()
            query = '''
                    delete from note_files
                    where note_UUID = %s and file_name = %s;
                    '''
            cursor.execute(query, (note_UUID, file_name))
            connection.commit()
        finally:
            if cursor:
                cursor.close()
