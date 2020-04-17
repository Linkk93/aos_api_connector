def get_interfaces(depth=1, **kwargs):
    target_url = kwargs["url"] + "system/interfaces?depth={}".format(depth)
    r = kwargs["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_lldp(interface: str, attributes='mac_addr,port_id,chassis_id,neighbor_info', depth=2, **kwargs):
    interface = interface.replace('/', '%2F')
    target_url = kwargs["url"] + "system/interfaces/{}/lldp_neighbors?attributes={}&depth={}".format(interface, attributes, depth)
    r = kwargs["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


