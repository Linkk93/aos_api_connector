import requests
import os


def _get_ca_bundle():
    # requests uses it's own CA bundle by default
    # but ADCS servers often have certificates
    # from private CAs that are locally trusted,
    # so we try to find, and use, the system bundle
    # instead. Fallback to requests own.
    """Tries to find the platform ca bundle for the system (on linux systems)"""
    ca_bundles = [
        # list taken from https://golang.org/src/crypto/x509/root_linux.go
        "/etc/ssl/certs/ca-certificates.crt",  # Debian/Ubuntu/Gentoo etc.
        "/etc/pki/tls/certs/ca-bundle.crt",  # Fedora/RHEL 6
        "/etc/ssl/ca-bundle.pem",  # OpenSUSE
        "/etc/pki/tls/cacert.pem",  # OpenELEC
        "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",  # CentOS/RHEL 7
    ]
    for ca_bundle in ca_bundles:
        if os.path.isfile(ca_bundle):
            return ca_bundle
    # if the bundle was not found, don't validate
    return False


def login(base_url, username=None, password=None) -> requests.Session:
    s = requests.Session()
    target_url = base_url + f"login?username={username}&password={password}"
    try:
        r = s.post(target_url, verify=False, timeout=5)
        if not r.ok:
            print(f"FAIL: Login failed with status code {r.status_code}")
            exit(-1)
        else:
            print("SUCCESS: Login succeeded")
            return s
    except requests.exceptions.ConnectTimeout:
        print('ERROR: Error connecting to host: connection attempt timed out.')
        exit(-1)


def logout(**session_dict):
    """
    Perform a POST call to logout and end session.

    :param session_dict:
        keyword s: requests.session object with loaded cookie jar
        keyword url: URL in main function example: "https://172.16.66.5/rest/v10.04/"
    :return: Nothing
    """
    r = session_dict["s"].post(session_dict["url"] + "logout", verify=False)
    if not r.ok:
        print(f"FAIL: Logout failed with status code {r.status_code}")
    else:
        print("SUCCESS: Logout succeeded")
