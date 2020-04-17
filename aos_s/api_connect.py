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
        return
    except requests.exceptions.ConnectTimeout:
        print('ERROR: Error connecting to host: connection attempt timed out.')
        exit(-1)


def logout(api_user='admin', **session_dict):
    target_url = session_dict['url'] + "login-sessions"
    header = {"SessionId": session_dict["cookie"]}
    data = json.dumps({'userName': api_user})
    r = session_dict['s'].delete(target_url, headers=header, data=data, verify=False)
    if r.ok:
        print("Logout {} successful! \n".format(session_dict['url']))
        return
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return
