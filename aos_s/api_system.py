

def get_system(**session_dict):
    target_url = session_dict['url'] + 'system'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_system_info(**session_dict):
    target_url = session_dict['url'] + 'system/status'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
