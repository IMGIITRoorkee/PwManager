from database import User, Key
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
import hashlib

class UserHandler:
    def __init__(self, session):
        self.session = session

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        password_hash = self.hash_password(password)
        key_value = Fernet.generate_key().decode()
        new_user = User(user_name=username, user_password=password_hash)
        self.session.add(new_user)
        self.session.commit()

        user_key = Key(key_value=key_value, user_id=new_user.user_id)
        self.session.add(user_key)
        self.session.commit()

    def authenticate_user(self, username, password):
        password_hash = self.hash_password(password)
        user = self.session.query(User).filter_by(user_name=username, user_password=password_hash).first()
        return user
