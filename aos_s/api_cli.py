import json


def post_command(command: str, **session_dict):
    # Single CLI command string. All configuration and execution commands in non-interactive mode are supported.
    # crypto, copy, process-tracking, recopy, redo, repeat, session, end, print,  terminal, logout, menu, page, restore,
    # update, upgrade-software, return,  setup, screen-length, vlan range and help commands are not supported.
    # Testmode commands are not supported. All show commands are supported except show tech and show history.
    command_dict = {"cmd": command}
    target_url = session_dict['url'] + f'cli'
    cookies = {'sessionId': session_dict["cookie"]}
    data = json.dumps(command_dict)
    r = session_dict['s'].post(target_url, cookies=cookies, data=data, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
