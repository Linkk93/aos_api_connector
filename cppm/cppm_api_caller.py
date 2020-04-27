from ..cppm import cppm_session, network_device


class CPPMAPIClient(object):
    def __init__(self, **kwargs):
        """
        :param kwargs:
            api_version: (str) API version, default v1
            username: (str) username for API login *
            password: (str) password for API login *
            protocol: (str) http or https, default https
            url: (str) IP or hostname *
            verify: (bool) https certificate verification, default False

            grant_type (string) = ['client_credentials' or 'password' or 'refresh_token']: OAuth2 authentication method,
            client_id (string): Client ID defined in API Clients,
            client_secret (string, optional): Client secret, required if the API client is not a public client,
            username (string, optional): Username for authentication, required for grant_type "password",
            password (string, optional): Password for authentication, required for grant_type "password",
            scope (string, optional): Scope of the access request,
            refresh_token (str, optional): Refresh token issued to the client, required for grant_type "refresh_token"

            * required
        """
        self.api_version = kwargs.get('api_version', 'v1')
        self.protocol = kwargs.get('protocol', 'https')
        self.url = kwargs['url']
        self.client_id = kwargs['client_id']
        self.grant_type = kwargs['grant_type']
        self.verify = kwargs.get('verify', False)

        self.session = None
        self.response = None
        self.session_dict = {}
        self.base_url = f'{self.protocol}://{self.url}/api/'

        if self.grant_type == 'client_credentials':
            self.client_secret = kwargs['client_secret']
        elif self.grant_type == 'password':
            self.username = kwargs['username']
            self.password = kwargs['password']
            self.client_secret = kwargs.get('client_secret', None)

    def connect(self):
        try:
            if self.grant_type == 'client_credentials':
                connection = cppm_session.login_credentials(self.base_url, self.client_id, self.client_secret)
            else:
                connection = cppm_session.login_password(self.base_url, self.client_id, self.username, self.password,
                                                         self.client_secret)
            self.session = connection['s']
            self.session_dict = connection
            self.session_dict['url'] = self.base_url

        except Exception as error:
            print(f'Ran into exception: {error}.')

    def get_all_network_devices(self):
        self.response = network_device.get_all_nd(**self.session_dict)
        return self.response

    def post_nd(self, nd_info):
        self.response = network_device.post_new_nd(nd_info, **self.session_dict)
        return self.response
