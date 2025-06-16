class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    def get_by_UUID(self, user_UUID):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_UUID = %s;', (user_UUID, ))
            return cursor.fetchone()
    
    def create_user(self, user_name, password, email):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                insert into users (UUID, user_name, user_email, user_password_hash)
                values (UUID(), %s, %s, sha2(%s, 256))
            '''
            user_data = (user_name, email, password)
            cursor.execute(query, user_data)
            connection.commit()
    
    def update_user(self, user_UUID, user_name, password, email):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                update users 
                set user_name = %s,
                    user_email = %s,
                    user_password_hash = sha2(%s, 256)
                where user_UUID = %s;
            '''
            user_data = (user_name, email, password, user_UUID)
            cursor.execute(query, user_data)
            connection.commit()
    
    def delete_user(self, user_UUID):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                    delete from users
                    where user_UUID = %s;
                    '''
            cursor.execute(query, (user_UUID, ))
            connection.commit()
