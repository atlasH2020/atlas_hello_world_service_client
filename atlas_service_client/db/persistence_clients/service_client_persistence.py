from service_client.db.persistence_clients.service_client_persistence import \
    AbstractServiceClientPersistence
from atlas_service_client.db.sql_app import schemas, crud


class PostgresServiceClientPersistence(AbstractServiceClientPersistence):

    def get_service_registration_id(self, client_id, client_secret):
        pass

    def get_service_registration_data_by_auth_url(self, oauth2_auth_url):
        return crud.ServiceRegistration.get_by_auth_url(oauth2_auth_url)

    def get_service_registration_data_by_registration_id(self, service_registration_id):
        return crud.ServiceRegistration.get_by_registration_id(service_registration_id)

    def persist_client_registration_info(self, oauth2_auth_url, client_id, client_secret):
        service_registration = schemas.ServiceRegistrationCreate(authorization_service_url=oauth2_auth_url,
                                                                 client_id=client_id,
                                                                 client_secret=client_secret)
        crud.ServiceRegistration.add(service_registration)

    def get_oauth2_code_flow_state(self, state_id):
        oauth2_code_flow = crud.OAuth2CodeFlowState.get_by_id(state_id)
        return oauth2_code_flow

    def persist_oauth2_authorization_code_flow_data(self, state_id, service_id, service_name, oauth2_auth_url,
                                                    oauth2_token_url):
        oauth2_code_flow_state = schemas.OAuth2GrantCodeFlowStateCreate(state_id=state_id, service_id=service_id,
                                                                        service_name=service_name,
                                                                        oauth2_auth_url=oauth2_auth_url,
                                                                        oauth2_token_url=oauth2_token_url)
        crud.OAuth2CodeFlowState.add(oauth2_code_flow_state)

    def delete_oauth2_authorization_code_flow(self, state_id):
        crud.OAuth2CodeFlowState.delete(state_id)

    def update_user_token(self, user_token_id, access_token, refresh_token):
        crud.UserToken.update(user_token_id, access_token, refresh_token)

    def persist_user_token(self, user_id, access_token, access_token_expires_in, refresh_token,
                           refresh_token_expires_in, registration_id):
        user_token = schemas.UserTokenCreate(user_id=user_id, refresh_token=refresh_token,
                                             access_token=access_token,
                                             access_token_expires_in=access_token_expires_in,
                                             refresh_token_expires_in=refresh_token_expires_in,
                                             registration_id=registration_id)
        crud.UserToken.add(user_token)

    def delete_user_token(self, user_id, registration_id):
        crud.UserToken.delete(user_id, registration_id)

    def get_user_token_data_by_id(self, user_token_id):
        return crud.UserToken.get_by_token_id(user_token_id)

    def get_user_token_data(self, user_id, registration_id):
        user_token = crud.UserToken.get_by_user_and_registration_id(user_id, registration_id)
        return user_token

    def get_user_services_by_id(self, service_id):
        user_services_result = crud.UserServices.get_by_service_id(service_id)
        return user_services_result

    def get_user_services_by_user_and_services_id(self, user_id, service_id):
        user_services_result = crud.UserServices.get_by_user_id_and_service_id(user_id, service_id)
        return user_services_result

    def get_user_services(self, user_id, service_name):
        user_services_result = crud.UserServices.get_by_user_id_and_service_name(user_id, service_name)
        return user_services_result

    def persist_user_services(self, service_id, service_name, user_id, user_token_id):
        user_services = schemas.UserServicesCreate(service_id=service_id, user_id=user_id,
                                                   service_name=service_name, user_token_id=user_token_id)
        crud.UserServices.add(user_services)

    def delete_service_from_user_services(self, user_token_id):
        crud.UserServices.delete(user_token_id)
