from __future__ import annotations
from abc import ABC, abstractmethod

from service_client.service_client import AbstractServiceClient
from service_client.db.persistence_clients.service_client_persistence import AbstractServiceClientPersistence
import requests
import json


class AbstractHelloWorldServiceClient(ABC):

    @abstractmethod
    def get_oauth2_auth_url(self):
        pass

    @abstractmethod
    def get_service_client_persistence(self):
        pass

    @abstractmethod
    def pair_service(self):
        pass

    @abstractmethod
    def systems_paired(self):
        pass

    @abstractmethod
    def pair_systems(self):
        pass

    @abstractmethod
    def service_endpoint_authentication(self):
        pass

    @abstractmethod
    def trigger_oauth2_authorization_code_flow(self):
        pass

    @abstractmethod
    def finalize_oauth2_authorization_code_flow(self, code, state, service_registration_id, oauth2_token_url, user_id,
                                                service_name):
        pass

    @abstractmethod
    def request_new_access_token(self, service_id, refresh_token, client_id, client_secret, user_token_id):
        pass

    @abstractmethod
    def check_response(self, response, service_id, user_token_id, refresh_token):
        pass

    @abstractmethod
    def get_data(self, service_id, user_token_id):
        pass


class HelloWorldServiceClient(AbstractHelloWorldServiceClient):
    # Favor object composition over inheritance. Leads to more flexible design.
    service_client: AbstractServiceClient
    service_client_persistence: AbstractServiceClientPersistence

    def __init__(self, service_client: AbstractServiceClient):
        self.service_client = service_client
        self.service_client_persistence = service_client.get_service_client_persistence()
        self.hello_world_url = service_client.get_service_base_url() + '/data'

    def get_oauth2_auth_url(self):
        return self.service_client.get_oauth2_auth_url()

    def get_service_client_persistence(self):
        return self.service_client.get_service_client_persistence()

    def pair_service(self):
        return self.service_client.pair_service()

    def systems_paired(self):
        return self.service_client.systems_paired()

    def pair_systems(self):
        return self.service_client.pair_systems()

    def service_endpoint_authentication(self):
        self.service_client.service_endpoint_authentication()

    def trigger_oauth2_authorization_code_flow(self):
        return self.service_client.trigger_oauth2_authorization_code_flow()

    def finalize_oauth2_authorization_code_flow(self, code, state, service_registration_id, oauth2_token_url, user_id,
                                                service_name):
        self.service_client.finalize_oauth2_authorization_code_flow(code, state, service_registration_id,
                                                                    oauth2_token_url, user_id, service_name)

    def request_new_access_token(self, service_id, refresh_token, client_id, client_secret, user_token_id):
        return self.service_client.request_new_access_token(service_id, refresh_token, client_id, client_secret,
                                                            user_token_id)

    def check_response(self, response, service_id, user_token_id, refresh_token):
        new_access_token = None
        if response.status_code == 200:
            return 'Success', new_access_token
        else:
            res_info = json.loads(response.text)
            print(res_info)
            if res_info['code'] == 'token_expired':
                print('requesting new access token')
                credentials = self.service_client_persistence.get_service_registration_data_by_auth_url(
                    self.service_client.get_oauth2_auth_url())
                new_access_token = self.request_new_access_token(service_id, refresh_token, credentials.client_id,
                                                                 credentials.client_secret, user_token_id)
                print('Going to print new access token')
                print(new_access_token)

                if new_access_token is None:
                    print('token not active, initiate service pairing')
                    self.service_client_persistence.delete_service_from_user_services(service_id)
                    self.pair_service()
                    return 'RePairing', None
                return 'NewToken', new_access_token
            else:
                print('ERROR requesting data', res_info)
                return 'Fail', None

    def get_data(self, service_id, user_token_id):
        self.hello_world_url = self.service_client.get_service_base_url()
        user_token_data = self.service_client_persistence.get_user_token_data_by_id(user_token_id)
        access_token = user_token_data.access_token
        refresh_token = user_token_data.refresh_token
        hdr = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        prms = {}
        resp = requests.get(self.hello_world_url+'/data', headers=hdr, params=prms, verify=True, allow_redirects=False)

        response_status, new_token = self.check_response(resp, service_id, user_token_id, refresh_token)

        if response_status == 'Success':
            return json.loads(resp.text)['data']
        elif response_status == 'RePairing':
            return {}
        elif response_status == 'NewToken':
            print('re-request data with new access token')
            hdr['Authorization'] = 'Bearer ' + new_token
            resp = requests.get(self.hello_world_url, headers=hdr, params=prms, verify=True, allow_redirects=False)
            res_info = json.loads(resp.text)
            data = json.loads(resp.text)['data']
            return data
        elif response_status == 'Fail':
            return {}
