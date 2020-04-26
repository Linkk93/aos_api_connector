

def get_system(**session_dict):
    target_url = session_dict['url'] + 'system'
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_system_info(**session_dict):
    target_url = session_dict['url'] + 'system/status'
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
