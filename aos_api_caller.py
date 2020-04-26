from aos_s import api_connect, api_cert, api_system, api_vlan, api_vlan_port, api_radius, api_snmpv3, api_ntp, api_timesync


def create_vlan_table(vlan_port_dict: dict):
    int_dict = {}
    for vlan_port in vlan_port_dict:
        # is interface new?
        if vlan_port['port_id'] not in int_dict.keys():
            int_dict[vlan_port['port_id']] = {'untagged': [], 'tagged': [], 'forbidden': []}

        if vlan_port['port_mode'] == 'POM_UNTAGGED':
            untag_list = int_dict[vlan_port['port_id']]['untagged']
            untag_list.append(vlan_port['vlan_id'])
            int_dict[vlan_port['port_id']]['untagged'] = untag_list
        elif vlan_port['port_mode'] == 'POM_TAGGED_STATIC':
            tag_list = int_dict[vlan_port['port_id']]['tagged']
            tag_list.append(vlan_port['vlan_id'])
            int_dict[vlan_port['port_id']]['tagged'] = tag_list
        elif vlan_port['port_mode'] == 'POM_FORBIDDEN':
            forbid_list = int_dict[vlan_port['port_id']]['forbidden']
            forbid_list.append(vlan_port['vlan_id'])
            int_dict[vlan_port['port_id']]['forbidden'] = forbid_list
    return int_dict


def _save(out_data, out_file):
    # write to file
    with open(out_file, 'w+') as file:
        file.write(str(out_data))


class AOSSwitchAPIClient(object):
    """
    attributes:
        api_version: (str) API version, default v7
        username: (str) username for API login *
        password: (str) password for API login *
        protocol: (str) http or https, default https
        url: (str) IP or hostname *
        verify: (bool) https certificate verification, default False

        * required
    """

    def __init__(self, **kwargs):
        self.api_version = kwargs.get('api_version', 'v7')
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.protocol = kwargs.get('protocol', 'https')
        self.url = kwargs['url']
        self.verify = kwargs.get('verify', False)
        self.session_dict = {}
        self.base_url = f'{self.protocol}://{self.url}/rest/{self.api_version}/'
        self.session = None
        self.response = None
        self.system_info = None
        self.vlan_info = None

    def connect(self):
        try:
            self.session = api_connect.login(self.base_url, self.username, self.password)
            self.session_dict = dict(s=self.session['s'], cookie=self.session['cookie'], url=self.base_url, ip=self.url)
        except Exception as error:
            print(f'Ran into exception: {error}.')
            raise error

    def disconnect(self):
        self.response = api_connect.logout(self.username, **self.session_dict)
        return self.response

    def get_ta_profile(self):
        self.response = api_cert.get_ta_profiles(**self.session_dict)
        return self.response

    def install_ta_profile(self, ta_profile):
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

        ta_response = api_cert.post_ta_profile(ta_profile, **self.session_dict)
        return ta_response

    def generate_csr(self, subject_dict, cert_name, ta_name):
        """
        attributes:
            example_subject_dict = {
                "common_name": "Switch_2540",
                "country": "DE",
                "locality": "Langenhagen",
                "organisation_name": "AirIT",
                "organisation_unit": "IT",
                "state": "DE"
            }
            cert_name: certificate name
            ta_name: existend TA / CA on the switch, with which the certificate will be signed
        """
        csr = api_cert.generate_csr(subject_dict, cert_name, ta_name, **self.session_dict)
        _save(csr, f'pki/json/{cert_name}.json')
        csr_decoded = api_cert.decode64(csr["certificate_detail_base64_encoded"])
        _save(csr_decoded, f'pki/csr/{cert_name}.csr')

    def post_signed_cert(self, signed_file_path):
        with open(signed_file_path, 'r') as file:
            cert_signed = file.read()
        cert_signed_b64 = api_cert.encode64(cert_signed)
        cert_install = api_cert.post_signed(cert_signed_b64, **self.session_dict)
        print(f'Certificate installed:\n{cert_install}\n')

    def get_vlans(self):
        self.response = api_vlan.get_all_vlan(**self.session_dict)
        return self.response

    def add_vlan(self, vlan_id, name, is_jumbo: bool = False, is_voice: bool = False, is_dhcp_snoop: bool = False,
                 is_dhcp_server: bool = False, is_mgmt_vlan: bool = False):
        self.response = api_vlan.add_vlan(vlan_id, name, is_jumbo, is_voice, is_dhcp_snoop, is_dhcp_server,
                                          is_mgmt_vlan, **self.session_dict)
        return self.response

    def get_vlan_port(self):
        self.response = api_vlan_port.get_vlan_ports(**self.session_dict)
        self.vlan_info = create_vlan_table(self.response)
        return self.response

    def get_system_info(self):
        self.system_info = api_system.get_system_info(**self.session_dict)
        self.system_info['ip'] = self.session_dict['ip']
        self.system_info['hostname'] = self.system_info['name']
        return self.system_info

    def new_radius_server(self, secret, address, auth_port=1812, acc_port=1813, **kwargs):
        self.response = api_radius.new_server(secret, address, auth_port, acc_port, **self.session_dict)
        return self.response

    def get_snmpv3_user(self):
        self.response = api_snmpv3.get_users(**self.session_dict)
        return self.response.json()

    def new_snmpv3_user(self, username: str, auth_pw: str, priv_pw: str, auth_prot: str = "sha", priv_prot: str = "aes",
                        v3_group: str = 'SGT_MANAGERPRIV', ):
        self.response = api_snmpv3.post_user(username, auth_pw, priv_pw, auth_prot, priv_prot, v3_group,
                                             **self.session_dict)
        return self.response

    def delete_snmpv3_user(self, username):
        self.response = api_snmpv3.delete_user(username, **self.session_dict)
        return self.response

    def get_snmpv3_params(self):
        self.response = api_snmpv3.get_params(**self.session_dict)
        return self.response.json()

    def new_snmpv3_params(self, name, username, sec_model="v3", message_model="v3", auth_type="priv"):
        self.response = api_snmpv3.post_params(name, username, sec_model, message_model, auth_type, **self.session_dict)
        return self.response

    def delete_snmpv3_params(self, name):
        self.response = api_snmpv3.delete_params(name, **self.session_dict)
        return self.response

    def enable_snmpv3(self):
        self.response = api_snmpv3.put_snmpv3_global(True, **self.session_dict)
        return self.response

    def disable_snmpv3(self):
        self.response = api_snmpv3.put_snmpv3_global(False, **self.session_dict)
        return self.response

    def get_ntp_global(self):
        self.response = api_ntp.get_ntp_global(**self.session_dict)
        return self.response.json()

    def put_ntp_global(self, enable: bool, is_broadcast: bool = True, max_association=8):
        self.response = api_ntp.put_ntp_global(enable, is_broadcast, max_association, **self.session_dict)
        return self.response

    def get_ntp_server(self, address=''):
        self.response = api_ntp.get_ntp_server(address, **self.session_dict)
        return self.response.json()

    def delete_ntp_server(self, address):
        self.response = api_ntp.delete_ntp_server(address, **self.session_dict)
        return self.response

    def new_ntp_server(self, address, min_pol=6, max_pol=10, is_burst=False, is_iburst=False, is_oobm=False):
        self.response = api_ntp.post_ntp_server(address, min_pol, max_pol, is_burst, is_iburst, is_oobm, **self.session_dict)
        return self.response

    def get_timesynch(self):
        self.response = api_timesync.get_timesynch(**self.session_dict)
        return self.response.json()

    def put_timesynch(self, sntp=False, timep=False, timep_or_sntp=True, ntp=False):
        self.response = api_timesync.put_timesynch(sntp, timep, timep_or_sntp, ntp, **self.session_dict)
        return self.response
