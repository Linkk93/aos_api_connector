import json


def generate_csr(cert_json: json, **session_dict):
    """
    :param cert_json:  dict containing cert info
    :param session_dict: API Session
    :return: bool: True if successfully created, False if error
    Example:
        cert_json = {
                    "cert_type": "regular"
                    "certificate_name": "new_cert"
                    "key_size": 2048
                    "key_type": "RSA"
                     "subject": {
                        "common_name": ""
                        "country": "DE"
                        "locality": ""
                        "org": ""
                        "org_unit": ""
                        "state": ""
                        }
                    }
    """
    target_url = session_dict["url"] + "certificates"
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
    }
    data = cert_json
    r = session_dict['s'].post(target_url, headers=headers, data=data, verify=False)
    if r.ok:
        return r.ok
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r.ok


def get_single_cert(cert_name, **kwargs):
    target_url = kwargs['url'][:-5] + '/' + f'certificates/{cert_name}'
    r = kwargs['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r


def get_certs(depth=3, **kwargs):
    target_url = kwargs["url"] + f'certificates&depth={depth}'
    r = kwargs['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r


def del_cert(cert_name, **kwargs):
    target_url = kwargs["url"] + f'certificates/{cert_name}'
    r = kwargs['s'].delete(target_url, verify=False)
    if r.ok:
        return r.content
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r


def put_cert(cert_name, cert_pem, **kwargs):
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
    }
    target_url = kwargs["url"] + f'certificates/{cert_name}'
    data = json.dumps({"certificate": cert_pem})
    r = kwargs['s'].put(target_url, headers=headers, data=data, verify=False)
    if r.ok:
        return r.content
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r


def put_trust():
    pass


def get_trust():
    pass
