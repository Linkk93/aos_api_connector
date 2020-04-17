import json


def get_all_vlan(**session_dict):
    target_url = session_dict['url'] + 'vlans'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()['vlan_element']
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_vlan(vlan_id, **session_dict):
    target_url = session_dict['url'] + f'vlans/{vlan_id}'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def post_new_vlan(vlan_id: int, name: str, is_jumbo: bool = False, is_voice: bool = False, is_dhcp_snoop: bool = False,
                  is_dhcp_server: bool = False, is_mgmt_vlan: bool = False, **session_dict):
    vlan_dict = {
        "vlan_id": vlan_id,
        "name": name,
        "is_jumbo_enabled": is_jumbo,
        "is_voice_enabled": is_voice,
        "is_dsnoop_enabled": is_dhcp_snoop,
        "is_dhcp_server_enabled": is_dhcp_server,
        "is_management_vlan": is_mgmt_vlan
    }
    target_url = session_dict['url'] + f'vlans'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps(vlan_dict)
    r = session_dict['s'].post(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def update_vlan(vlan_id: int, name='', is_jumbo: bool = False, is_voice: bool = False, is_dhcp_snoop: bool = False,
                is_dhcp_server: bool = False, is_mgmt_vlan: bool = False, **session_dict):
    vlan_dict = {
        "vlan_id": vlan_id,
        "name": name,
        "is_jumbo_enabled": is_jumbo,
        "is_voice_enabled": is_voice,
        "is_dsnoop_enabled": is_dhcp_snoop,
        "is_dhcp_server_enabled": is_dhcp_server,
        "is_management_vlan": is_mgmt_vlan
    }
    target_url = session_dict['url'] + f'vlans/{vlan_id}'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps(vlan_dict)
    r = session_dict['s'].put(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def delete_vlan(vlan_id: int, **session_dict):
    target_url = session_dict['url'] + f'vlans/{vlan_id}'
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].delete(target_url, cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def add_vlan(vlan_id: int, name: str, is_jumbo: bool = False, is_voice: bool = False, is_dhcp_snoop: bool = False,
             is_dhcp_server: bool = False, is_mgmt_vlan: bool = False, **session_dict):
    vlan_dict = get_all_vlan(**session_dict)
    vlan_str = f'/vlans/{vlan_id}'
    for vlan in vlan_dict:
        if vlan_str == vlan['uri']:
            r = update_vlan(vlan_id, name, is_jumbo, is_voice, is_dhcp_snoop, is_dhcp_server, is_mgmt_vlan,
                            **session_dict)
            return r
    r = post_new_vlan(vlan_id, name, is_jumbo, is_voice, is_dhcp_snoop, is_dhcp_server, is_mgmt_vlan, **session_dict)
    return r
