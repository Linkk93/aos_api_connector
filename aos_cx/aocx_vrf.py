

def get_vrf(depth=3, attributes: str = 'attributes=name,dns_domain_list,snmp_status,status,dns_name_servers,'
                                       'dns_domain_name,ssh_enable,https_server,dhcp_server,ospf_routers,pim_routers,'
                                       'snmp_enable,type,vrf_address_families,ssh_sessions,routes', **session_dict):
    target_url = session_dict["url"] + "system/vrfs?attributes={}&depth={}".format(attributes, depth)
    r = session_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
