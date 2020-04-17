import json


def new_name(port, port_name, **session_dict):
    print("Changing name of port {} to {}\n".format(port, port_name))
    cookies = {'sessionId': session_dict["cookie"]}
    json_name = json.dumps({'id': port, 'name': port_name})
    r = session_dict['s'].put(session_dict['url'] + f"/ports/{port}", cookies=cookies, data=json_name,
                              verify=False)
    if r.ok:
        print("Change successful!\n")
        return
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return
