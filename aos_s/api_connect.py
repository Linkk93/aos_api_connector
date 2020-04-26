import requests
import json


def login(api_url, api_user=None, api_pw=None):
    print("Getting cookie")
    s = requests.Session()
    target_url = api_url + "login-sessions"
    data = json.dumps({'userName': api_user, 'password': api_pw})
    try:
        r = s.post(target_url, data=data, verify=False)
        if r.ok:
            return {'s': s, 'cookie': r.json()['cookie'].split('=')[1]}
        else:
            print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r
    except requests.exceptions.ConnectTimeout as e:
        print('ERROR: Error connecting to host: connection attempt timed out.')
        raise e


def logout(api_user, **session_dict):
    target_url = session_dict['url'] + "login-sessions"
    data = json.dumps({'userName': api_user})
    r = session_dict['s'].delete(target_url, data=data, verify=False)
    if r.ok:
        print("Logout {} successful! \n".format(session_dict['url']))
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r
