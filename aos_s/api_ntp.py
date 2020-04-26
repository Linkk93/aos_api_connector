import json


def get_ntp_global(**session_dict):
    r = session_dict['s'].get(session_dict['url'] + "config/ntp", verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def put_ntp_global(enable: bool, is_broadcast: bool = True, max_association=8, **session_dict):
    data = json.dumps({
        'broadcast': is_broadcast,
        'max-association': {'max-association_value': max_association},
        'enable': enable})

    r = session_dict['s'].put(session_dict['url'] + "config/ntp", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def get_ntp_server(address='', **session_dict):
    if address != '':
        target_url = f"{session_dict['url']}config/ntp/server/ip4addr/{address}"
    else:
        target_url = session_dict['url'] + "config/ntp/server/ip4addr"
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def post_ntp_server(address, min_pol=6, max_pol=10, is_burst=False, is_iburst=False, is_oobm=False, **session_dict):
    data = {'ip4addr': {'ip4addr_value': address,
                        'ip4addr_reference': {'min-poll': {'min-poll_value': min_pol},
                                              'max-poll': {'max-poll_value': max_pol}}}}
    if is_iburst and not is_burst:
        data['iburst'] = True
    elif is_burst and not is_iburst:
        data['iburst'] = True

    data = json.dumps(data)
    r = session_dict['s'].post(session_dict['url'] + "config/ntp/server/ip4addr", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def delete_ntp_server(address, **session_dict):
    r = session_dict['s'].delete(session_dict['url'] + f"config/ntp/server/ip4addr/{address}", verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r
