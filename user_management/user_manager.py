import functools

from passlib.context import CryptContext
from atlas_service_client.db.db_client import db_client
from atlas_service_client.db.db_context import DBContext
import starlette.status as status
from fastapi import Request

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserManager:

    def __init__(self):
        self.user_persistence = db_client(DBContext.User_Management)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def register_user(self, username, password):

        user_fetched = self.user_persistence.fetch_user(username)
        if not user_fetched:
            password_hashed = self.get_password_hash(password)
            self.user_persistence.store_user(username, password_hashed)
            return True
        else:
            return False

    def login_user(self, username, password):
        user_fetched = self.user_persistence.fetch_user(username)
        if user_fetched:
            result = self.verify_password(password, user_fetched.pass_word)
            if result:
                return True
            else:
                return False
        else:
            return False

    def get_user_name(self):
        return self.username


def user_manager_factory():
    return UserManager()
