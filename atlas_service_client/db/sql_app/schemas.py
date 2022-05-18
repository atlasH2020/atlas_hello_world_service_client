from typing import List, Optional

from pydantic import BaseModel
from . import models

'''User Management Base Schemas'''


class UserBase(BaseModel):
    user_name: str
    hashed_password: str


class UserCreate(UserBase):
    pass


'''OAuth Base Schemas'''


class UserTokenBase(BaseModel):
    user_id: int
    refresh_token: str
    access_token: str
    access_token_expires_in: str
    refresh_token_expires_in: str
    registration_id: int


class UserServicesBase(BaseModel):
    user_id: int
    service_id: str
    service_name: str
    user_token_id: int


class ServiceRegistrationBase(BaseModel):
    authorization_service_url: str
    client_id: str
    client_secret: str


class OAuth2GrantCodeFlowStateBase(BaseModel):
    state_id: str
    service_id: str
    service_name: str
    oauth2_auth_url: str
    oauth2_token_url: str


'''OAuth Create Schemas'''


class UserTokenCreate(UserTokenBase):
    pass


class UserServicesCreate(UserServicesBase):
    pass


class ServiceRegistrationCreate(ServiceRegistrationBase):
    pass


class OAuth2GrantCodeFlowStateCreate(OAuth2GrantCodeFlowStateBase):
    pass


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class UserToken(UserTokenBase):
    user_token_id: int

    class Config:
        orm_mode = True


class ServiceRegistration(ServiceRegistrationBase):
    registration_id: int

    class Config:
        orm_mode = True