from aos_cx import aocx_interfaces, aocx_cert, aocx_system, aocx_vlan, aocx_vrf, aocx_session
import json


class AOSCXAPIClient(object):
    def __init__(self, **kwargs):
        """
        :param kwargs:
            api_version: (str) API version, default v7
            username: (str) username for API login *
            password: (str) password for API login *
            protocol: (str) http or https, default https
            url: (str) IP or hostname *
            verify: (bool) https certificate verification, default False

            * required
        """
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

    def disconnect(self):
        return aocx_session.logout(**self.session_dict)

    def connect(self):
        try:
            self.session = aocx_session.login(self.base_url, self.username, self.password)
            self.session_dict = dict(s=self.session, url=self.base_url, ip=self.url)
        except Exception as error:
            print(f'Ran into exception: {error}. Logging out..')

    def backup_file(self, file_path, config: str):
        c = aocx_system.get_config(config, **self.session_dict)
        with open(file_path, 'w+') as f:
            json.dump(c, f)

    def put_config(self, config_path, config_name):
        r = aocx_system.put_config(config_path, config_name, **self.session_dict)
        return r

    def get_config(self, config_name):
        r = aocx_system.get_config(config_name, **self.session_dict)
        return r

    def get_vlans(self):
        vlan_info = aocx_vlan.get_vlans(**self.session_dict)
        return vlan_info

    def get_temperature(self):
        temp_info = aocx_system.temperature(**self.session_dict)
        return temp_info

    def get_interfaces(self):
        interface_info = aocx_interfaces.get_interfaces(**self.session_dict)
        return interface_info

    def get_int_lldp(self, interface):
        lldp_dict = aocx_interfaces.get_lldp(interface, **self.session_dict)
        return lldp_dict

    def new_csr(self, cert_dict):
        """
        :param cert_dict:
            example_cert_dict = {
                'cert_type': 'regular',
                 'certificate_name': 'new_cert',
                 'key_size': 2048,
                 'key_type': 'RSA',
                 'subject': {
                 'common_name': 'SW01-RZ1',
                 'country': 'DE',
                 'locality': 'Langenhagen',
                 'org': 'AirIT',
                 'org_unit': 'IT',
                 'state': 'Nds'}}
        :return: Signing request, empty string if error
        """
        # format csr to json
        cert_json = json.dumps(cert_dict)
        # generate CSR, but it's still on the switch; True if successful
        bool_create = aocx_cert.generate_csr(cert_json, **self.session_dict)
        if bool_create:
            # get CSR from switch
            csr = aocx_cert.get_single_cert(cert_dict['certificate_name'], **self.session_dict)
            return csr['certificate']
        else:
            print('CSR could not be created.\n')
            return ''

    def put_ca(self, ca_file):
        with open(ca_file, 'r') as f:
            ca = f.read()
        aocx_cert.put_cert('lab-ca', ca, **self.session_dict)

    def put_signed(self, signed_file, cert_name):
        with open(signed_file, 'r') as f:
            signed = f.read()
        aocx_cert.put_cert(cert_name, signed, **self.session_dict)

    def get_system_info(self):
        system_info_dict = aocx_system.get_system_info_all(**self.session_dict)
        system_info_dict['ip'] = self.session_dict['ip']
        return system_info_dict

    def get_subsystem_info(self):
        subsystem_info = aocx_system.subsystem_info(**self.session_dict)
        return subsystem_info

    def get_version(self):
        version_info = aocx_system.version(**self.session_dict)
        return version_info

    def get_vrf_info(self):
        vrf_info = aocx_vrf.get_vrf(**self.session_dict)
        return vrf_info
