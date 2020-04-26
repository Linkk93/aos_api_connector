import json


def _map_oper_mode(mode):
    if mode == 'unicast':
        return "SNTP_UNICAST_MODE"
    elif mode == 'broadcast':
        return "SNTP_BROADCAST_MODE"
    elif mode == 'dhcp':
        return "SNTP_DHCP_MODE"
    elif mode == 'disable':
        return "SNTP_DISABLE"


def get_sntp_global(**session_dict):
    target_url = session_dict['url'] + "system/sntp"
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def put_sntp_global(oper_mode='unicast', poll_interval=720, **session_dict):
    """
    :param oper_mode: one of: 'unicast', 'broadcast', 'dhcp', 'disable'
    :param poll_interval:
    :param session_dict:
    :return:
    """
    oper_mode = _map_oper_mode(oper_mode)
    data = json.dumps({"sntp_client_operation_mode": oper_mode,
                       "sntp_config_poll_interval": poll_interval})
    target_url = session_dict['url'] + "system/sntp"
    r = session_dict['s'].put(target_url, data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r
