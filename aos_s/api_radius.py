import json


def get_servers(**session_dict):
    target_url = session_dict['url'] + f"radius_servers"
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return


def new_server(secret, address, auth_port=1812, acc_port=1813, dyn_auth=True, **session_dict):
    radius_dict = {"address": {"version": "IAV_IP_V4",
                               "octets": address},
                   "shared_secret": secret,
                   "authentication_port": auth_port,
                   "accounting_port": acc_port,
                   "is_dyn_authorization_enabled": dyn_auth,
                   "time_window_type": "TW_POSITIVE_TIME_WINDOW",
                   "time_window": 300,
                   "is_oobm": False
                   }

    target_url = session_dict['url'] + f"radius_servers"
    data = json.dumps(radius_dict)
    r = session_dict['s'].post(target_url, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return


def update_server(radius_server: dict, **session_dict):
    pass


def delete_server(**session_dict):
    pass
