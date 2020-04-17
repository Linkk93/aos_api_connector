import json
from datetime import datetime
import base64


def decode64(encoded: str) -> str:
    decoded = base64.b64decode(encoded).decode('UTF-8').replace('\r', '')
    return decoded


def encode64(decoded: str) -> str:
    encoded = base64.b64encode(decoded.encode()).decode('UTF-8')
    return encoded


def get_ta_profiles(**session_dict):
    target_url = session_dict['url'] + 'ta_profiles'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_ta_profile(profile, **session_dict):
    target_url = session_dict['url'] + 'ta_profiles'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps(profile)
    r = session_dict['s'].post(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def generate_csr(subject_dict, cert_name, ca_name='Default', **session_dict):
    target_url = session_dict['url'] + '/crypto_pki/create_csr'
    # cert_usages = [
    #    "CA_OPENFLOW",
    #    "CA_WEB",
    #    "CA_CAPTIVE_PORTAL",
    #    "CA_SSH_CLIENT",
    #    "CA_SSH_SERVER",
    #    "CA_SYSLOG",
    #    "CA_ALL",
    #    "CA_IDEVID"
    # ]

    now = datetime.now()
    month_list = [
        "M_JANUARY",
        "M_FEBRUARY",
        "M_MARCH",
        "M_APRIL",
        "M_MAY",
        "M_JUNE",
        "M_JULY",
        "M_AUGUST",
        "M_SEPTEMBER",
        "M_OCTOBER",
        "M_NOVEMBER",
        "M_DECEMBER"
    ]
    cur_month = month_list[now.month - 1]

    valid_from = {
        "year": now.year,
        "month": cur_month,
        "day_of_month": now.day
    }

    valid_until = {
        "year": now.year + 3,
        "month": cur_month,
        "day_of_month": now.day
    }

    csr_validity = {
        "validity_start_date": valid_from,
        "validity_end_date": valid_until
    }

    csr_dict = {
                "certificate_name": cert_name,
                "ta_profile": ca_name,
                "subject": subject_dict,
                "cert_usage": "CA_WEB",
                "validity": csr_validity
            }
    data = json.dumps(csr_dict)
    header = {"cookie": session_dict["cookie"]}
    r = session_dict['s'].post(target_url, data=data, headers=header, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_local(cert_name, **session_dict):
    target_url = session_dict['url'] + f'crypto_pki/local_certificate/{cert_name}'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def delete_cert(cert_name, **session_dict):
    target_url = session_dict['url'] + f'crypto_pki/local_certificate/{cert_name}'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].delete(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_signed(cert, **session_dict):
    target_url = session_dict['url'] + 'crypto_pki/install_signed_certificate'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps({"signed_certificate_base64_encoded_pem": cert})
    r = session_dict['s'].post(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
