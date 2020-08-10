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
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_ta_profile(profile, **session_dict):
    # Example
    # example_ca_cert =
    """-----BEGIN CERTIFICATE-----
    MIIDlTCCAn2gAwIBAgIQMgtXkI1Gj79IP/hQ/QgJqDANBgkqhkiG9w0BAQ0FADBd
    MRUwEwYKCZImiZPyLGQBGRYFbG9jYWwxHjAcBgoJkiaJk/IsZAEZFg5nYWxsaXNj
    aGVzZG9yZjEkMCIGA1UEAxMbZ2FsbGlzY2hlc2RvcmYtTEFCU0VSVkVSLUNBMB4X
    DTE2MTEwMjE2MzkyNVoXDTI2MTEwMjE2NDkyNFowXTEVMBMGCgmSJomT8ixkARkW
    BWxvY2FsMR4wHAYKCZImiZPyLGQBGRYOZ2FsbGlzY2hlc2RvcmYxJDAiBgNVBAMT
    G2dhbGxpc2NoZXNkb3JmLUxBQlNFUlZFUi1DQTCCASIwDQYJKoZIhvcNAQEBBQAD
    ggEPADCCAQoCggEBAN7LN8ZSWS7anCppVnrEAGXZg9IMxWj4/mzzrPN9rJvQ0VvM
    +eP4B9h6YYKPusM4fsDFgtL1mzFe/X+d/tDC+yNMeJqij5enEQOEZd2iM8k9l/Wc
    jkfqO3xcTk2v/ZWyuPJx9NSN/3Ib/RfFsS8VTQdbmUvVoFc8NqoHrvMm8cbILKU6
    Ql6z3aG1m/3hJSWQSiJa8PC2w6azPiF9ueslHKGh30gPq8N6yCQg1FFJA/lqQrPS
    geJdBIt31Lf/gcfCxY/p4/nF2DfG/lFCR/SoNgRAOVJKfx7HabRt2JOtPPDJo7jd
    w84M03U7eXKzhPzhmn1VIr9AlLc0i9v3w4bHMCcCAwEAAaNRME8wCwYDVR0PBAQD
    AgGGMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFIWssVZFpHds3gfwzF9ZOKZy
    ymAVMBAGCSsGAQQBgjcVAQQDAgEAMA0GCSqGSIb3DQEBDQUAA4IBAQBD6UvJiHqL
    5zxSkScf01koSN69qFe+NCa94IHIMRtwXh/OVtecfZZbVZmwXoLzA0EJLhdtSyXt
    6Fnvca/9QLhNCnPsPH3wcoqfaCu4OXLhlMABTiPq5Q2WYQKRougzXhljC6MTMgEE
    n+4yuEA7RoK2TzLkaIkDFiGsKt0/0kjq1JNvvAWaw4PwziCeaT4KR3gvTjKkPypZ
    Rt2jijBe8Uf03lvC/gb5BC4ibEo/ylYoJm5bu/yY8802DGTqzk4JmvaBb0MMRSsl
    Yc+IyB1SINArLD4jtoYYeDZadgQUcu9sNJyFaZxT3w2lmsYgQ5hc3MPCpyy/5NI5
    uEqKFsAOZjR/
    -----END CERTIFICATE-----
    """

    """
    example_ta_profile = {
        "ta_name": 'gallischesdorf-LABSERVER-CA',
        "ta_certificate_base64_encoded_pem": api_cert.encode64(example_ca_cert)
    }
    """
    target_url = session_dict['url'] + 'ta_profiles'
    data = json.dumps(profile)
    r = session_dict['s'].post(target_url, data=data, verify=False)
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
    r = session_dict['s'].post(target_url, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_local(cert_name, **session_dict):
    target_url = session_dict['url'] + f'crypto_pki/local_certificate/{cert_name}'
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def delete_cert(cert_name, **session_dict):
    target_url = session_dict['url'] + f'crypto_pki/local_certificate/{cert_name}'
    r = session_dict['s'].delete(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_signed(cert, **session_dict):
    target_url = session_dict['url'] + 'crypto_pki/install_signed_certificate'
    data = json.dumps({"signed_certificate_base64_encoded_pem": cert})
    r = session_dict['s'].post(target_url, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
