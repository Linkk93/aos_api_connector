import json


def get_all(**session_dict):
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(session_dict['url'] + "snmpv3", cookies=cookies, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def put_snmpv3_global(enabled: bool, readonly=False, messages=False, **session_dict):
    # Disabling SNMPv3 deletes all users!
    snmpv3_data = {
        'is_snmpv3_server_enabled': enabled,
        'is_non_snmpv3_access_readonly': readonly,
        'is_snmpv3_messages_only': messages}
    data = json.dumps(snmpv3_data)
    r = session_dict['s'].put(session_dict['url'] + "snmpv3", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r

# #############  USER #############


def _map_user(auth_prot: str, priv_prot: str) -> dict:
    # map authentication protocol
    if auth_prot.lower() == "md5":
        auth_prot = "SAP_MD5"
    elif auth_prot.lower() == "sha":
        auth_prot = "SAP_SHA"
    elif auth_prot.lower() == "none":
        auth_prot = "SAP_NONE"
    # map privacy protocol
    if priv_prot.lower() == "des":
        priv_prot = "SAPP_DES"
    elif priv_prot.lower() == "aes":
        priv_prot = "SAPP_AES"
    elif priv_prot.lower() == "none":
        priv_prot = "SAPP_NONE"

    return {"auth_prot": auth_prot,
            "priv_prot": priv_prot}


def get_users(**session_dict):
    r = session_dict['s'].get(session_dict['url'] + "snmpv3/users", verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def post_user(username: str, auth_pw: str, priv_pw: str, auth_prot: str = "sha", priv_prot: str = "aes",
              v3_group: str = 'SGT_MANAGERPRIV', **session_dict):
    # creates a new user, error if user exists
    params = _map_user(auth_prot, priv_prot)

    user_data = {
        'user_name': username,
        'snmpv3_authentication_protocol': params["auth_prot"],
        'authentication_password': auth_pw,
        'snmpv3_authentication_privacy_protocol': params["priv_prot"],
        'privacy_password': priv_pw,
        'snmpv3_v3_group': v3_group}
    data = json.dumps(user_data)

    r = session_dict['s'].post(session_dict['url'] + "snmpv3/users", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def put_user(username: str, auth_pw: str, priv_pw: str, auth_prot: str = "sha", priv_prot: str = "aes",
             v3_group: str = 'SGT_MANAGERPRIV', **session_dict):
    # updates an existing user
    params = _map_user(auth_prot, priv_prot)

    user_data = {
        'user_name': username,
        'snmpv3_authentication_protocol': [params["auth_prot"]],
        'authentication_password': auth_pw,
        'snmpv3_authentication_privacy_protocol': [params["priv_prot"]],
        'privacy_password': priv_pw,
        'snmpv3_v3_group': v3_group}
    data = json.dumps(user_data)

    r = session_dict['s'].put(session_dict['url'] + "snmpv3/users", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def delete_user(username, **session_dict):
    r = session_dict['s'].delete(session_dict['url'] + f"snmpv3/users/{username}", verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r

# #############  Params #############


def _map_params(sec_model, message_model, auth_type) -> dict:
    # map Snmpv3 sec-model
    if sec_model.lower() == "v1":
        sec_model = "SSM_VER1"
    elif sec_model.lower() == "v2c":
        sec_model = "SSM_VER2C"
    elif sec_model.lower() == "v3":
        sec_model = "SSM_VER3"
    # map Snmpv3 message processing model value
    if message_model.lower() == "v1":
        message_model = "SMPMV_VER1"
    elif message_model.lower() == "v2c":
        message_model = "SMPMV_VER2C"
    elif message_model.lower() == "v3":
        message_model = "SMPMV_VER3"
    # map Snmpv3 message processing model value
    if auth_type.lower() == "auth":
        auth_type = "ATV_AUTH"
    elif auth_type.lower() == "priv":
        auth_type = "ATV_PRIV"
    elif auth_type.lower() == "none":
        auth_type = "ATV_NOAUTH"

    return {"sec_model": sec_model,
            "message_model": message_model,
            "auth_type": auth_type}


def get_params(**session_dict):
    r = session_dict['s'].get(session_dict['url'] + "snmpv3/params", verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def post_params(name, username, sec_model="v3", message_model="v3", auth_type="priv", **session_dict):
    # create new params
    params = _map_params(sec_model, message_model, auth_type)
    user_data = {
        'parameter_name': name,
        'user_name': username,
        'snmpv3_sec_model': [params["sec_model"]],
        'snmpv3_message_processing_model_value': [params["message_model"]],
        'snmpv3_authentication': [params["auth_type"]]}
    data = json.dumps(user_data)

    r = session_dict['s'].post(session_dict['url'] + "snmpv3/params", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def put_params(name, username, sec_model="v3", message_model="v3", auth_type="priv", **session_dict):
    # update existing params
    params = _map_params(sec_model, message_model, auth_type)
    user_data = {
        'parameter_name': name,
        'user_name': username,
        'snmpv3_sec_model': [params["sec_model"]],
        'snmpv3_message_processing_model_value': [params["message_model"]],
        'snmpv3_authentication': [params["auth_type"]]}
    data = json.dumps(user_data)

    r = session_dict['s'].put(session_dict['url'] + f"snmpv3/params/{name}", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def delete_params(name, **session_dict):
    r = session_dict['s'].delete(session_dict['url'] + f"snmpv3/users{name}", verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r
