from testcase.multiplay.default import Default
from testcase.multiplay.exec_request import ExecRequest


def test_hello():
    url = Default.endpoint + '/v1/identity/hello'
    message = Default.random_letters()
    resp = ExecRequest.send_request('post', url,
                                    {'Content-Type': 'application/json'},
                                    {'name': message})
    assert resp.status_code == 200
    assert resp.json()['message'] == message + ' world'
    print(type(resp.json()))


def test_auth():
    create_auth_key_url = Default.endpoint + '/v1/identity/auth-keys'
    ExecRequest.send_request('post', create_auth_key_url,
                             {'Content-Type': 'application/json'},
                             {'note': 'randomstring', 'orgId': Default.random_letters()})
