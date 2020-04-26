import json


def get_radius_vrf(vrf, depth=0, **sesion_dict):
    target_url = sesion_dict["url"] + "system/vrfs/{}/radius_servers?depth={}".format(vrf, depth)
    r = sesion_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_radius_server(secret, address, auth_port=1812, acc_port=1813, vrf_name='default', group='radius',
                       default_group_prio: int = 1, **sesion_dict):
    """
    :param secret: RADIUS shared secret
    :param address: RADIUS server adress
    :param default_group_prio:
    :param group:
    :param auth_port:
    :param acc_port:
    :param vrf_name:
    :param sesion_dict:
    :return: session return
    Creates dict to send to switch: dict with RADIUS server parameters:
            {
              "accounting_udp_port": 1813,
              "udp_port": 1812,
              "address": "192.168.87.31",
              "default_group_priority": 1,
              "passkey": "RADIUS_secret"
              "group": [
                "/rest/v10.04/system/aaa_server_groups/radius"
              ],
              "vrf": "/rest/v10.04/system/vrfs/default"
            }
    """

    vrf_uri = f'/rest/v10.04/system/vrfs/{vrf_name}'
    target_url = sesion_dict['url'] + f"system/vrfs/{vrf_name}/radius_servers"

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }
    data = json.dumps({"default_group_priority": default_group_prio,
                       "group": [f"/rest/v10.04/system/aaa_server_groups/{group}"],
                       "passkey": secret,
                       "udp_port": auth_port,
                       "accounting_udp_port": acc_port,
                       "vrf": vrf_uri,
                       "address": address})
    try:
        r = sesion_dict['s'].post(target_url, data=data, headers=headers, verify=False)
        if r.ok:
            return r
        else:
            print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
            return {}
    except Exception as error:
        print(f'Error: {error}')
        raise error
