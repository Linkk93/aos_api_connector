import requests
import json


def login_credentials(base_url: str, client_id: str,  client_secret: str) -> dict:
    s = requests.Session()
    target_url = base_url + f"oauth"
    headers = {'Content-Type': 'application/json'}
    data = {'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret}
    return _post(s, target_url, headers, data, False)


def login_password(base_url: str, client_id: str, username: str, password: str, client_secret: str = None) -> dict:
    s = requests.Session()
    target_url = base_url + f"oauth"
    headers = {'Content-Type': 'application/json'}
    # with client secret
    if client_secret is not None:
        data = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'password': password,
            'username': username}
    # without client secret
    else:
        data = {
            'grant_type': 'password',
            'client_id': client_id,
            'password': password,
            'username': username}
    return _post(s, target_url, headers, data, False)


def _post(session, target_url, headers, data, verify=False):
    try:
        r = session.post(target_url, headers=headers, data=json.dumps(data), verify=verify)
        if not r.ok:
            print(f"FAIL: Login failed with status code {r.status_code}")
            raise ConnectionError
        else:
            body_json = json.loads(r.content.decode("UTF-8"))
            print("SUCCESS: Login succeeded")
            return {'s': session, **body_json}
    except requests.exceptions.ConnectTimeout:
        print('ERROR: Error connecting to host: connection timed out.')
        raise TimeoutError
    except Exception as e:
        raise e
