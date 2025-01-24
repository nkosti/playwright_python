import logging
import os
from typing import Literal
from urllib.parse import urljoin

import requests
import urllib3

from test.domains.test_data.dto.users.users_dto import UserDTO

# todo:
# break down and handle URLs to be flexible for other envs
# add a fixture initiating the api client in a seamless manner, similar to poms object
ENV_NAME = os.getenv("ENV_NAME")


class BaseRestClient:
    """
    Handles authentication by passed in credentials.
    Exposes a generic CRUD interface for other clients.
    """
    TEST_AUTH_URL = (f"https://test.{ENV_NAME}.com")

    def __init__(self, username, password):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.auth_url = self.TEST_AUTH_URL
        self.username = username
        self.password = password
        self.access_token = None
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification

    def authenticate(self):
        payload = (
            f'grant_type=password&scope=eead_scope&username={self.username}&password={self.password}')
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic Og=='}

        with self.session as session:
            logging.info(f"PAYLOAD: {payload}")

            response = session.post(self.auth_url, data=payload, headers=headers, verify=False)
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
        logging.info(f"User authenticated: {self.username}")

    def get_headers(self, content_type="application/json"):
        """Return default headers including authorization token"""
        if not self.access_token:  # Authenticate if token is missing
            self.authenticate()

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": content_type
        }

    def _request(self, method: Literal["get", "post", "put", "delete"], endpoint_url: str = None, **kwargs):
        """
        Customize requests with different keyword arguments
        """
        headers = self.get_headers()

        with self.session as session:
            request_kwargs = {
                "url": endpoint_url,
                "headers": headers,
                "timeout": 10,
                **kwargs
            }
            response = getattr(session, method)(**request_kwargs)
            logging.info(f'RESPONSE: {response.text}')
            response.raise_for_status()  # Raises HTTPError if status code is 4xx/5xx
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                logging.info(f"Cannot decode JSON. Response: {response.text}")
                return response

    def get(self, endpoint: str, **kwargs):
        return self._request('get', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request('post', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request('put', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request('delete', endpoint, **kwargs)


class UsersAPIClient(BaseRestClient):
    BASE_URL = f"https://test.{ENV_NAME}.com/api/"
    USERS_ENDPOINT = urljoin(BASE_URL, "users/")

    def create_user(self, user_payload):
        return self.post(self.USERS_ENDPOINT, json=user_payload)

    def update_user(self, user_id, user_payload):
        return self.put(f"{self.USERS_ENDPOINT}{user_id}/", json=user_payload)

    def delete_user(self, user_id):
        return self.delete(f"{self.USERS_ENDPOINT}{user_id}/")

    def create_user_from_dto(self, user_info: UserDTO, **kwargs):
        default_payload = {
            "email": user_info.email,
            "organizationId": "ORGID",  # DOP id
            "phoneNumber": user_info.phone_no,
            "firstName": user_info.first_name,
            "lastName": user_info.last_name,
            "userName": user_info.username
        }

        # Overwrite payload with extra keyword arguments
        # todo remove DOP as default org as workaround after UOM-2221 is fixed
        payload = {**default_payload, **kwargs}
        logging.info("CREATING USER")
        logging.info(f"PAYLOAD{payload}")
        new_user = self.create_user(payload)
        user_id = new_user["userId"]
        from test.conftest import EnvData

        upd_payload = {**payload, "organizationId": EnvData.orgs[user_info.org_name]}
        logging.info("UPDATING USER")
        logging.info(f"UPD_PAYLOAD{upd_payload}")
        upd_org_user = self.update_user(user_id, upd_payload)
        return upd_org_user


class OrganizationsAPIClient(BaseRestClient):
    BASE_URL = f"https://test.{ENV_NAME}.com/api/"
    ORGANIZATIONS_ENDPOINT = urljoin(BASE_URL, "organizations/")
    ALL_ORGANIZATIONS_ENDPOINT = urljoin(BASE_URL, "public/organizations/list/")

    def create_organization(self, organization_payload):
        return self.post(self.ORGANIZATIONS_ENDPOINT, json=organization_payload)

    def delete_organization(self, org_id: str):
        return self.delete(f"{self.ORGANIZATIONS_ENDPOINT}{org_id}/")

    def get_organizations(self):
        payload = {
            "parentOrgId": "ParentOrgId",  # call with a DOP superuser to get all organizations
            "includeSubOrganizations": True,
            "paging": {
                "limit": 100,
                "offset": 0
            },
            "filter": {},
            "sort": {
                "sortAttribute": "name",
                "sortAscending": True
            }
        }
        return self.post(self.ALL_ORGANIZATIONS_ENDPOINT, json=payload)


class RolesAPIClient(BaseRestClient):
    BASE_URL = f"https://uom-uom-api.{ENV_NAME}.com/api/"
    ROLES_ENDPOINT = urljoin(BASE_URL, "roles/")
    ROLES_LIST_ENDPOINT = urljoin(BASE_URL, "internal/roles/list/")

    def create_role(self, role_payload):
        return self.post(self.ROLES_ENDPOINT, json=role_payload)

    def get_roles(self):
        payload = {"paging": {"limit": 100, "offset": 0}}
        return self.post(self.ROLES_LIST_ENDPOINT, json=payload)

    def delete_role(self, role_id):
        return self.delete(f"{self.ROLES_ENDPOINT}{role_id}/")


class APIClients:
    def __init__(self, username="batman@dc.com", password="batman@dc.com"):
        self.users = UsersAPIClient(username, password)
        self.organizations = OrganizationsAPIClient(username, password)
        self.roles = RolesAPIClient(username, password)
