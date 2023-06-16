import json
import logging
from sys import platform

import requests

from testcase.multiplay.default import Default


class ExecRequest:
    logger = logging.getLogger('request logging')

    @staticmethod
    def send_request(req_method, req_url, req_headers, req_body, resp_code=200):
        logging.info(str(req_method).upper() + ': ' + req_url)
        if req_headers is not None:
            actual_headers = {**req_headers, **Default.get_basic_auth()}
        else:
            actual_headers = Default.get_basic_auth()
        if platform == "darwin":
            logging.info('Request header: ' + json.dumps(actual_headers, indent=4, sort_keys=True))
        else:
            logging.info('Request header: ' + json.dumps(req_headers, indent=4, sort_keys=True))
        logging.info('Request body  : ' + json.dumps(req_body, indent=4))
        response = ''
        if str(req_method).upper() == 'POST':
            response = requests.post(req_url, json=req_body, headers=actual_headers)
        elif str(req_method).upper() == 'GET':
            response = requests.get(req_url, json=req_body, headers=actual_headers)
        elif str(req_method).upper() == 'PUT':
            response = requests.put(req_url, json=req_body, headers=actual_headers)
        elif str(req_method).upper() == 'PATCH':
            response = requests.patch(req_url, json=req_body, headers=actual_headers)
        elif str(req_method).upper() == 'DELETE':
            response = requests.delete(req_url, json=req_body, headers=actual_headers)

        logging.info('Response status code: ' + str(response.status_code))

        try:
            logging.info('Response body: ' + json.dumps(response.json(), indent=4))
        finally:
            assert response.status_code == resp_code
        return response
