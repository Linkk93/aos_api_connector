

def get_all(**session_dict):
    print("Getting all LLDP neighbors")
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(session_dict['url'] + "lldp/remote-device", cookies=cookies, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return


def print_lldp(lldp_data):
    for n in lldp_data['lldp_remote_device_element']:
        print("#############################################")
        print(f"Local Port: \t\t {n['local_port']}")
        print(f"Remote Port: \t\t {n['port_id']}")
        print(f"Remote Device: \t\t {n['system_name']}")
        print(f"Remote ID: \t\t\t {n['chassis_id']}")
        print("#############################################\n")
