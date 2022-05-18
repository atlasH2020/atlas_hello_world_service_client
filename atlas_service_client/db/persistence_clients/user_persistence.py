from __future__ import annotations
from abc import ABC, abstractmethod

from atlas_service_client.db.sql_app import crud, schemas

class AbstractUserPersistence(ABC):

    @abstractmethod
    def fetch_user(self, username):
        pass

    @abstractmethod
    def fetch_user_by_id(self, user_id):
        pass

    @abstractmethod
    def store_user(self, username, password_hashed):
        pass



class PostgresUserPersistence(AbstractUserPersistence):

    def fetch_user(self, username):
        return crud.User.get_user(username)

    def fetch_user_by_id(self, user_id):
        return crud.User.get_user_by_id(user_id)

    def store_user(self, username, password_hashed):
        new_user = schemas.UserCreate(user_name=username, hashed_password=password_hashed)
        crud.User.add(new_user)
