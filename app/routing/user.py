from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.user_UUID = user_data['user_UUID']
        self.user_name = user_data['user_name']
        self.user_email = user_data['user_email']
        self.user_data = user_data
