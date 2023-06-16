import base64
import json
import logging
import requests
import common.utility


class HttpClient:
    logger = logging.getLogger('HttpClient')
    headers = {'Content-Type': 'application/json'}
    default_genesis_url, default_cloud_platform_url, default_play_platform_url, properties, \
        resource_file_path = common.utility.read_config()

    def __init__(self):
        super().__init__()

    def get_service_token(self):
        service_client_key = self.properties.get('serviceClient')
        client_secret = self.properties.get('serviceSecret')
        self.headers['Authorization'] = 'Basic ' + str(
            base64.b64encode((service_client_key + ':' + client_secret).encode('utf-8')), 'utf-8')

    def get_smoke_token(self):
        smoke_client_key = self.properties.get('defaultClient')
        smoke_secret = self.properties.get('defaultSecret')
        self.headers['Authorization'] = 'Basic ' + str(
            base64.b64encode((smoke_client_key + ':' + smoke_secret).encode('utf-8')), 'utf-8')

    def get_access_token(self, user_email, pwd):
        payload = {
            'grant_type': 'PASSWORD',
            'username': user_email,
            'password': pwd,
            'client_id': self.properties.get('defaultClient'),
            'client_secret': self.properties.get('defaultSecret')
        }

        response = self.send_post_request_with_json(self.default_genesis_url + '/oauth2/token', json=payload,
                                                    req_headers=self.headers, req_cookies=None)
        return response.json()['access_token']

    def get_authorization_info(self, user_email, pwd):
        payload = {
            'grant_type': 'PASSWORD',
            'username': user_email,
            'password': pwd,
            'client_id': self.properties.get('defaultClient'),
            'client_secret': self.properties.get('defaultSecret')
        }

        response = self.send_post_request_with_json(self.default_genesis_url + '/oauth2/token', json=payload,
                                                    req_headers=self.headers, req_cookies=None)
        return response.json()

    @staticmethod
    def send_requests(req_method, server_url, req_body, req_headers, req_cookies):
        logging.info('URL:  ' + server_url)
        logging.info('Header:' + str(req_headers))
        logging.info('Request Method:' + req_method)
        logging.info('Request body:  ' + json.dumps(req_body))
        logging.info('Request Cookies:' + str(req_cookies))
        response = ''
        if req_method == 'POST':
            response = requests.post(server_url, json=req_body, headers=req_headers, cookies=req_cookies)
        elif req_method == 'GET':
            response = requests.get(server_url, json=req_body, headers=req_headers, cookies=req_cookies)
        elif req_method == 'PUT':
            response = requests.put(server_url, json=req_body, headers=req_headers, cookies=req_cookies)
        elif req_method == 'PATCH':
            response = requests.patch(server_url, json=req_body, headers=req_headers, cookies=req_cookies)
        elif req_method == 'DELETE':
            response = requests.delete(server_url, json=req_body, headers=req_headers, cookies=req_cookies)

        logging.info('response status code is: ' + str(response.status_code))

        try:
            logging.info('Response body: ' + str(response.json()))
        finally:
            return response

    @staticmethod
    def send_requests_without_cookie(req_method, server_url, req_body, req_headers):
        logging.info('URL:  ' + server_url)
        logging.info('Header:' + str(req_headers))
        logging.info('Request body:  ' + json.dumps(req_body))
        response = ''
        if req_method == 'POST':
            response = requests.post(server_url, json=req_body, headers=req_headers)
        elif req_method == 'GET':
            response = requests.get(server_url, json=req_body, headers=req_headers)
        elif req_method == 'PUT':
            response = requests.put(server_url, json=req_body, headers=req_headers)
        elif req_method == 'PATCH':
            response = requests.patch(server_url, json=req_body, headers=req_headers)
        elif req_method == 'DELETE':
            response = requests.delete(server_url, json=req_body, headers=req_headers)

        logging.info('response status code is: ' + str(response.status_code))

        try:
            logging.info('Response body: ' + str(response.json()))
        finally:
            return response

    @staticmethod
    def send_get_request_with_params(server_url, params, req_headers, req_cookies):
        logging.info('URL:  ' + server_url)
        logging.info('Header:' + str(req_headers))
        logging.info('params:' + str(params))
        response = requests.get(server_url, params=params, headers=req_headers, cookies=req_cookies)

        logging.info('response status code is: ' + str(response.status_code))
        try:
            logging.info('Response body: ' + str(response.json()))
        finally:
            return response

    @staticmethod
    def send_post_request_with_data_file(server_url, data, files, req_headers, req_cookies):
        logging.info('URL:  ' + server_url)
        logging.info('Headers:' + str(req_headers))
        response = requests.post(server_url, data=data, files=files, headers=req_headers, cookies=req_cookies)

        logging.info('response status code is: ' + str(response.status_code))
        try:
            logging.info('Response body: ' + str(response.json()))
        finally:
            return response

    @staticmethod
    def send_put_request_with_data_file(server_url, data, files, req_headers, req_cookies):
        logging.info('URL:  ' + server_url)
        logging.info('Headers:' + str(req_headers))
        response = requests.put(server_url, data=data, files=files, headers=req_headers, cookies=req_cookies)

        logging.info('the put response status code is: ' + str(response.status_code))
        try:
            logging.info('Response body: ' + str(response.json()))
        finally:
            return response

    @staticmethod
    def send_post_request_with_json(server_url, json, req_headers, req_cookies):
        logging.info('URL:  ' + server_url)
        logging.info('Headers:' + str(req_headers))
        response = requests.post(server_url, json=json, headers=req_headers, cookies=req_cookies)

        logging.info('response status code is: ' + str(response.status_code))
        try:
            logging.info('Response body: ' + str(response.json()))
        finally:
            return response
