from database import Database
from models.alerts.alert import Alert


class User(object):
    COLLECTION_NAME = 'users'

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def register_user(email,password):
        user_data = Database.find_one(User.COLLECTION_NAME, {"email":email})
        if user_data is None:
            User(email, password).save_to_db()
            return True

        return False


    def save_to_db(self):
        Database.insert(User.COLLECTION_NAME, self.json())


    def json(self):
        return {
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def is_login_valid(email,password):
        user_data = Database.find_one(User.COLLECTION_NAME, {"email": email})
        if user_data:
            if user_data['password'] == password:
                return True



        return False

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)

    @classmethod
    def find_by_email(cls, email):
        #return cls(**Database.find_one(User.COLLECTION_NAME, {'email': email}))
        user = Database.find_one(User.COLLECTION_NAME, {'email':email})
        email = user['email']
        password = user['password']
        user = User(email,password)
        return user


