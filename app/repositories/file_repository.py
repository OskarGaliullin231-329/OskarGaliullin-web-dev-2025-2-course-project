class FileRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_all_filenames_by_note_UUID(self, note_UUID):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('SELECT file_name FROM note_files WHERE note_UUID = %s;' (note_UUID, ))
            return cursor.fetchall()

    def add_file(self, file_name, note_UUID):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('''
                           insert into note_files (file_name, note_UUID)
                           values (%s, %s);
                           ''', (file_name, note_UUID))

    def delete_file(self, note_UUID ,file_name):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                    delete from note_files
                    where note_UUID = %s and file_name = %s;
                    '''
            cursor.execute(query, (note_UUID, file_name))
            connection.commit()
