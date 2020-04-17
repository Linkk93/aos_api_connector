import json


def get_vlan_ports(**session_dict):
    target_url = session_dict['url'] + 'vlans-ports'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()['vlan_port_element']
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_vlan_port(vlan_id: int, port_id: str, mode: str = 'POM_TAGGED_STATIC', **session_dict):
    vlan = {
        'vlan_id': vlan_id,
        'port_id': port_id,
        'port_mode': mode
    }
    target_url = session_dict['url'] + 'vlans-ports'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps(vlan)
    r = session_dict['s'].post(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def put_vlan_port(vlan_id: int, port_id: str, mode: str = 'POM_TAGGED_STATIC', **session_dict):
    vlan = {
        'vlan_id': vlan_id,
        'port_id': port_id,
        'port_mode': mode
    }
    target_url = session_dict['url'] + 'vlans-ports'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps(vlan)
    r = session_dict['s'].put(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def add_vlan_port(vlan_id: int, port_id: str, mode: str = 'POM_TAGGED_STATIC', **session_dict):
    vlan_port_dict = get_vlan_ports(**session_dict)
    vlan_port_str = f'/vlans-ports/{vlan_id}-{port_id}'
    for vlan_port in vlan_port_dict:
        if vlan_port_str == vlan_port['uri']:
            r = put_vlan_port(vlan_id, port_id, mode, **session_dict)
            return r
    r = post_vlan_port(vlan_id, port_id, mode, **session_dict)
    return r
