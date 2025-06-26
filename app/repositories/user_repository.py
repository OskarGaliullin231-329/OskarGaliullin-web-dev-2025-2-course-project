class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_by_UUID(self, user_UUID):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_UUID = %s;', (user_UUID, ))
            return cursor.fetchone()

    def get_UUID_by_username(self, user_name):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute('SELECT user_UUID FROM users WHERE user_name = %s;', (user_name, ))
            return cursor.fetchone()

    def get_by_username_and_password(self, user_name, password):
        with self.db_connector.connect().cursor() as cursor:
            query = '''
                SELECT * FROM users 
                WHERE (user_name = %s or user_email = %s) and 
                user_pass_hash = sha2(%s, 256);
            '''
            cursor.execute(query, (user_name, user_name, password))
            return cursor.fetchone()

    def create_user(self, user_name, password, email):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                insert into users (user_UUID, user_name, user_email, user_pass_hash)
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
                    user_pass_hash = sha2(%s, 256)
                where user_UUID = %s;
            '''
            user_data = (user_name, email, password, user_UUID)
            cursor.execute(query, user_data)
            connection.commit()
        
    def update_user_PE(self, user_UUID, password, email):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                update users 
                set user_email = %s,
                    user_pass_hash = sha2(%s, 256)
                where user_UUID = %s;
            '''
            user_data = (email, password, user_UUID)
            cursor.execute(query, user_data)
            connection.commit()
    
    def update_user_NE(self, user_UUID, user_name, email):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                update users 
                set user_name = %s,
                    user_email = %s
                where user_UUID = %s;
            '''
            user_data = (user_name, email, user_UUID)
            cursor.execute(query, user_data)
            connection.commit()
    
    def update_user_NP(self, user_UUID, user_name, password):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            query = '''
                update users 
                set user_name = %s,
                    user_pass_hash = sha2(%s, 256)
                where user_UUID = %s;
            '''
            user_data = (user_name, password, user_UUID)
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
