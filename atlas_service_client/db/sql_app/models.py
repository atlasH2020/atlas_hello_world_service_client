from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, REAL, TEXT, FLOAT
from sqlalchemy.orm import relationship

from .database import Base

'''User Tables'''


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True)
    pass_word = Column(String, nullable=False)
    children = relationship("UserTokens", cascade="all,delete", backref="users")


'''OAuth Tables'''


class UserTokens(Base):
    __tablename__ = "user_tokens"
    user_token_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=False)
    refresh_token = Column(String)
    access_token = Column(String)
    access_token_expires_in = Column(String)
    refresh_token_expires_in = Column(String)
    registration_id = Column(Integer, ForeignKey('services_registration.registration_id'), nullable=False, unique=False)
    children = relationship("UserServices", cascade="all,delete", backref="user_tokens")


class UserServices(Base):
    __tablename__ = "user_services"
    service_id = Column(String, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    service_name = Column(String, nullable=False)
    user_token_id = Column(Integer, ForeignKey('user_tokens.user_token_id'))


class ServiceRegistration(Base):
    __tablename__ = "services_registration"
    registration_id = Column(Integer, primary_key=True, index=True)
    authorization_service_url = Column(String, unique=True)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)


class OAuth2GrantCodeFlowState(Base):
    __tablename__ = "oauth2_grant_code_flow_state"
    state_id = Column(String, primary_key=True)
    service_id = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    oauth2_auth_url = Column(String, nullable=False)
    oauth2_token_url = Column(String, nullable=False)