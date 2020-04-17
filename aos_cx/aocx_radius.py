import json


def get_radius_vrf(vrf, depth=0, **sesion_dict):
    target_url = sesion_dict["url"] + "system/vrfs/{}/radius_servers?depth={}".format(vrf, depth)
    r = sesion_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def put_radius_server(radius: dict, **sesion_dict):
    """
    :param vrf:
    :param depth:
    :param radius: dict with minimum RADIUS server parameters: {
            'name': 'VRF identifier. Should be alphanumeric. VRF names must be unique.',
            'address': 'IPV4/IPV6 address or FQDN of the RADIUS server',
            'udp_port': 'Specifies the udp port number for authentication.',
            'passkey': 'Specifies the passkey between RADIUS client and RADIUS server for authentication.',
            'group': 'Specifies the RADIUS server-group that it belongs to. It would belong to a family group 'radius'
                group and the user defined AAA server group',
            }
    :param sesion_dict:
    :return:
    """
    target_url = sesion_dict["url"] + f"system/vrfs/{radius['name']}/radius_servers/{radius['address']},{radius['udp_port']}"

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }
    data = json.dumps({"default_group_priority": 1,
                       "group": ["radius"],
                       "passkey": radius['passkey'],
                       "udp_port": radius['udp_port'],
                       "vrf": radius['name']})

    r = sesion_dict["s"].put(target_url, data=data, header=headers, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}

