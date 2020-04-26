import json


def get_all_nd(**session_dict):
    target_url = f"{session_dict['url']}network-device"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"{session_dict['token_type']} {session_dict['access_token']}"
    }
    r = session_dict['s'].get(target_url, headers=headers, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return


def post_new_nd(nd_info: dict, **session_dict):
    target_url = f"{session_dict['url']}network-device"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"{session_dict['token_type']} {session_dict['access_token']}"
    }
    data = json.dumps(nd_info)
    r = session_dict['s'].post(target_url, headers=headers, data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return
