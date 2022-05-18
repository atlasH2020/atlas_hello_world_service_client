from __future__ import annotations
from abc import ABC, abstractmethod

from .persistence_clients.service_client_persistence import AbstractServiceClientPersistence
from .persistence_clients.service_client_persistence import PostgresServiceClientPersistence
from .persistence_clients.user_persistence import AbstractUserPersistence
from .persistence_clients.user_persistence import PostgresUserPersistence

from .db_context import DBContext
from .sql_app import models
from .sql_app.database import engine

models.Base.metadata.create_all(bind=engine)

'''
Uses abstract factory design pattern to create database clients.
PostgresUserPersistence and PostgresServiceClientPersistence are concrete dao products of different types.
DBHandler acts as the Abstract Factory containing factory methods to instantiate each product.
PostgresServiceClientPersistence: implements the interface for handling access to OAuth tables.
PostgresUserPersistence: implements the interface for handling access to User tables.

db_client is a callable object. Hence you can use the object like a function.
db_client(DBContext.Service_Client) will provide the service client persistence object.
'''


class DBHandler(ABC):

    @abstractmethod
    def retrieve_service_client_db_handler(self) -> AbstractServiceClientPersistence:
        pass


class SQLLiteDBHandler(DBHandler):

    def retrieve_service_client_db_handler(self) -> AbstractServiceClientPersistence:
        return PostgresServiceClientPersistence()

    def retrieve_user_manager_db_handler(self) -> AbstractUserPersistence:
        return PostgresUserPersistence()


class DBClientAccessor:
    db_client: DBHandler

    def __init__(self, db_handler):
        self.db_client = db_handler

    def get_service_client_db_client(self) -> AbstractServiceClientPersistence:
        return self.db_client.retrieve_service_client_db_handler()

    def get_user_manager_db_client(self) -> AbstractUserPersistence:
        return self.db_client.retrieve_user_manager_db_handler()

    def __call__(self, context: DBContext):
        if context == DBContext.Service_Client:
            return self.get_service_client_db_client()
        elif context == DBContext.User_Management:
            return self.get_user_manager_db_client()


db_client = DBClientAccessor(SQLLiteDBHandler())
