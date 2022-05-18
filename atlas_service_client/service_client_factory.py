from __future__ import annotations
from abc import ABC, abstractmethod

from service_client.service_client import ServiceClient
from service_client.service_client import AbstractServiceClient
from .db.db_client import db_client
from .db.db_context import DBContext
from .hello_world_service_client import AbstractHelloWorldServiceClient
from .hello_world_service_client import HelloWorldServiceClient
from .service_context import ServiceContext
from config import app


class AbstractServiceClientFactory(ABC):

    @abstractmethod
    def get_service_client(self, service_id, redirect_url):
        pass

    @abstractmethod
    def get_hello_world_service_client(self, service_id, redirect_url):
        pass


class ServiceClientFactory(AbstractServiceClientFactory):

    def get_service_client(self, service_id, redirect_url) -> AbstractServiceClient:
        service_client: AbstractServiceClient = ServiceClient(service_id, redirect_url)
        service_client.set_service_client_persistence(db_client(DBContext.Service_Client))
        return service_client

    def get_hello_world_service_client(self, service_id, redirect_url) -> AbstractHelloWorldServiceClient:
        service_client: AbstractServiceClient = ServiceClient(service_id, redirect_url)
        service_client.set_service_client_persistence(db_client(DBContext.Service_Client))
        return HelloWorldServiceClient(service_client)


class AtlasServiceClientAccessor:
    service_client_factory: AbstractServiceClientFactory

    def __init__(self, service_client_factory):
        self.service_client_factory = service_client_factory

    def __call__(self, *args, **kwargs):
        service_id = args[0]
        redirect_url = args[1]
        return self.service_client_factory.get_hello_world_service_client(service_id, redirect_url)


atlas_service_client = AtlasServiceClientAccessor(ServiceClientFactory())
