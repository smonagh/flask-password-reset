import os
from app import db
import jwt
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return 'User {}'.format(self.username)

    def set_password(self, password, commit=False):
        self.password_hash = generate_password_hash(password)

        if commit:
            db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.username, 'exp': time() + expires},
                           key=os.getenv('SECRET_KEY_FLASK'))

    @staticmethod
    def verify_reset_token(token):
        try:
            username = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
            print(username)
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username, password, email):

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return False

        user = User()

        user.username = username
        user.password = user.set_password(password)
        user.email = email

        db.session.add(user)
        db.session.commit()

        return True

    @staticmethod
    def login_user(username, password):

        user = User.query.filter_by(username=username).first()

        if user:
            if user.verify_password(password):
                return True

        return False

    @staticmethod
    def verify_email(email):

        user = User.query.filter_by(email=email).first()

        return user
