from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas


class MySuperContextManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


def get_db():
    with MySuperContextManager() as db:
        yield db


'''User Management CRUD'''


class User:

    @staticmethod
    def add(user: schemas.UserCreate, db: Session = SessionLocal()):
        db_user = models.Users(user_name=user.user_name, pass_word=user.hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()

    @staticmethod
    def get_user(user_name: str, db: Session = SessionLocal()):
        result = db.query(models.Users).filter(models.Users.user_name == user_name).first()
        db.close()
        return result

    @staticmethod
    def get_user_by_id(user_id: int, db: Session = SessionLocal()):
        result = db.query(models.Users).filter(models.Users.user_id == user_id).first()
        db.close()
        return result


'''OAuth Tables CRUD'''


class ServiceRegistration:

    @staticmethod
    def add(service_registration: schemas.ServiceRegistrationCreate,
            db: Session = SessionLocal()):
        db_service_registration = models.ServiceRegistration(
            authorization_service_url=service_registration.authorization_service_url,
            client_id=service_registration.client_id, client_secret=service_registration.client_secret)
        db.add(db_service_registration)
        db.commit()
        db.refresh(db_service_registration)
        db.close()

    @staticmethod
    def get_by_auth_url(authorization_service_URL: str, db: Session = SessionLocal()):
        result = db.query(models.ServiceRegistration).filter(
            models.ServiceRegistration.authorization_service_url == authorization_service_URL).first()
        db.close()
        return result

    @staticmethod
    def get_by_registration_id(service_registration_id: int, db: Session = SessionLocal()):
        result = db.query(models.ServiceRegistration).filter(
            models.ServiceRegistration.registration_id == service_registration_id).first()
        db.close()
        return result

    @staticmethod
    def get_all(db: Session = SessionLocal()):
        result = db.query(models.ServiceRegistration)
        db.close()
        return result


class UserToken:

    @staticmethod
    def add(user_token: schemas.UserTokenCreate, db: Session = SessionLocal()):
        db_user_token = models.UserTokens(user_id=user_token.user_id, refresh_token=user_token.refresh_token,
                                          access_token=user_token.access_token,
                                          access_token_expires_in=user_token.access_token_expires_in,
                                          refresh_token_expires_in=user_token.refresh_token_expires_in,
                                          registration_id=user_token.registration_id)
        db.add(db_user_token)
        db.commit()
        db.refresh(db_user_token)
        db.close()

    @staticmethod
    def update(user_token_id, access_token, refresh_token, db: Session = SessionLocal()):
        user_token_result = db.query(models.UserServices).filter(
            models.UserServices.user_token_id == user_token_id).first()
        if user_token_result is not None:
            user_token_result.access_token = access_token
            user_token_result.refresh_token = refresh_token
            db.commit()
        db.close()

    @staticmethod
    def get_by_token_id(user_token_id: int, db: Session = SessionLocal()):
        result = db.query(models.UserTokens).filter(models.UserTokens.user_token_id == user_token_id).first()
        print(result.access_token)
        db.close()
        return result

    @staticmethod
    def get_by_user_and_registration_id(user_id: int, registration_id: int, db: Session = SessionLocal()):
        result = db.query(models.UserTokens).filter(models.UserTokens.registration_id == registration_id,
                                                    models.UserTokens.user_id == user_id).first()
        db.close()
        return result

    @staticmethod
    def delete_by_token_id(user_token_id: int, db: Session = SessionLocal()):
        result = db.query(models.UserTokens).filter(models.UserTokens.user_token_id == user_token_id).first()
        if result is not None:
            db.delete(result)
            db.commit()
        db.close()

    @staticmethod
    def delete(user_id: int, registration_id: int, db: Session = SessionLocal()):
        user_token = db.query(models.UserTokens).filter(models.UserTokens.user_id == user_id,
                                                        models.UserTokens.registration_id == registration_id).first()
        if user_token is not None:
            db.delete(user_token)
            db.commit()
        db.close()


class UserServices:

    @staticmethod
    def add(user_services: schemas.UserServicesCreate, db: Session = SessionLocal()):
        db_user_service = models.UserServices(service_id=user_services.service_id, user_id=user_services.user_id,
                                              service_name=user_services.service_name,
                                              user_token_id=user_services.user_token_id)
        db.add(db_user_service)
        db.commit()
        db.refresh(db_user_service)
        db.close()

    @staticmethod
    def get_all_by_service_id(service_id: str, db: Session = SessionLocal()):
        result = db.query(models.UserServices).filter(models.UserServices.service_id == service_id)
        db.close()
        return result

    @staticmethod
    def get_by_service_id(service_id: str, db: Session = SessionLocal()):
        result = db.query(models.UserServices).filter(models.UserServices.service_id == service_id).first()
        db.close()
        return result

    @staticmethod
    def get_by_user_id_and_service_id(user_id:str, service_id: str, db: Session = SessionLocal()):
        result = db.query(models.UserServices).filter(models.UserServices.user_id == user_id,
                                                      models.UserServices.service_id == service_id).first()
        db.close()
        return result

    @staticmethod
    def get_by_user_id_and_service_name(user_id: str, service_name: str, db: Session = SessionLocal()):
        result = db.query(models.UserServices).filter(models.UserServices.user_id == user_id,
                                                      models.UserServices.service_name == service_name).first()
        db.close()
        return result

    @staticmethod
    def delete_by_service_id(service_id: str, db: Session = SessionLocal()):
        result = db.query(models.UserServices).filter(models.UserServices.service_id == service_id).first()
        if result is not None:
            db.delete(result)
            db.commit()
        db.close()

    @staticmethod
    def delete(user_token_id: str, db: Session = SessionLocal()):
        result = db.query(models.UserServices).filter(models.UserServices.user_token_id == user_token_id).first()
        if result is not None:
            db.delete(result)
            db.commit()
        db.close()


class OAuth2CodeFlowState:

    @staticmethod
    def add(oauth2_code_flow: schemas.OAuth2GrantCodeFlowStateCreate,
            db: Session = SessionLocal()):
        db_oauth2_code_flow_state = models.OAuth2GrantCodeFlowState(state_id=oauth2_code_flow.state_id,
                                                                    service_id=oauth2_code_flow.service_id,
                                                                    service_name=oauth2_code_flow.service_name,
                                                                    oauth2_auth_url=oauth2_code_flow.oauth2_auth_url,
                                                                    oauth2_token_url=oauth2_code_flow.oauth2_token_url)
        db.add(db_oauth2_code_flow_state)
        db.commit()
        db.refresh(db_oauth2_code_flow_state)
        db.close()

    @staticmethod
    def get_by_id(state_id: str, db: Session = SessionLocal()):
        result = db.query(models.OAuth2GrantCodeFlowState).filter(
            models.OAuth2GrantCodeFlowState.state_id == state_id).first()
        db.close()
        return result

    @staticmethod
    def delete(state_id: str, db: Session = SessionLocal()):
        oauth2_code_flow_state = db.query(models.OAuth2GrantCodeFlowState).filter(
            models.OAuth2GrantCodeFlowState.state_id == state_id).first()
        if oauth2_code_flow_state is not None:
            db.delete(oauth2_code_flow_state)
            db.commit()
        db.close()