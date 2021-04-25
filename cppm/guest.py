import random
import string


def post(target_url, body=None, **session_dict):
    if body is None:
        body = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"{session_dict['token_type']} {session_dict['access_token']}"
    }
    r = session_dict['s'].post(target_url, headers=headers, verify=False, json=body)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return


def patch(target_url, body=None, **session_dict):
    if body is None:
        body = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"{session_dict['token_type']} {session_dict['access_token']}"
    }
    r = session_dict['s'].patch(target_url, headers=headers, verify=False, json=body)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return


def get(target_url, **session_dict):
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


def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


def get_guest(guest_id: int, **session_dict):
    target_url = f"{session_dict['url']}guest/{guest_id}"
    return get(target_url, **session_dict)


def create_guest(**session_dict):
    target_url = f"{session_dict['url']}guest"
    body = {
        "enabled": True,
        'do_expire': 4,  # logout and delete after expiration
        "notes": "made by API",
        "username": random_string(),
        "password": random_string(),
        "role_id": 2,
        "simultaneous_use": 3
    }
    return post(target_url, body, **session_dict)


def update_guest_expiration(guest_id: int, expire_after: int = 8, **session_dict):
    target_url = f"{session_dict['url']}guest/{guest_id}"
    guest = get_guest(guest_id, **session_dict).json()
    expire_seconds = expire_after * 60 * 60
    expire_time = guest['start_time'] + expire_seconds
    body = {
        'expire_time': expire_time
    }
    return patch(target_url, body, **session_dict)


def get_receipt(guest_id: int, receipt_template_id: int = 5, **session_dict):
    target_url = f"{session_dict['url']}guest/{guest_id}/receipt/{receipt_template_id}"
    try:
        return get(target_url, **session_dict).json()['guest_receipt']
    except Exception as e:
        return
