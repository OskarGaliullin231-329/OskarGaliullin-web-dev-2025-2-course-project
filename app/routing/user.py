from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.user_name = user_data[1]
        self.user_email = user_data[2]
        self.user_data = user_data
