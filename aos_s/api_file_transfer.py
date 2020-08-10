import json
# TODO: work on File Transfer
# not implemented


def _map_image(image: str):
    if image.lower() == 'primary':
        return 'BI_PRIMARY_IMAGE'
    else:
        return 'BI_SECONDARY_IMAGE'


def _map_action(action: str):
    if action.lower() == 'download':
        return 'FTA_DOWNLOAD'
    else:
        return 'FTA_UPLOAD'


def _map_file_type(file_type: str):
    if file_type.lower() == 'config':
        return 'FTT_CONFIG'
    elif file_type.lower() == 'firmware':
        return 'FTT_FIRMWARE'
    if file_type.lower() == 'event_logs':
        return 'FTT_EVENT_LOGS'
    elif file_type.lower() == 'crash':
        return 'FTT_CRASH_FILES'
    if file_type.lower() == 'system_info':
        return 'FTT_SYSTEM_INFO'
    elif file_type.lower() == 'show_tech':
        return 'FTT_SHOW_TECH'
    else:
        return 'FTT_DEBUG_LOGS'


def post_file(file_path, boot_image='secondary', file_type='firmware', action='download', **session_dict):
    action = _map_action(action)
    file_type = _map_action(file_type)
    boot_image = _map_image(boot_image)
    user_data = {
        'file_type': file_type,
        'action': action,
        'boot_image': boot_image
    }
    data = json.dumps(user_data)

    r = session_dict['s'].post(session_dict['url'] + "file-transfer", data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def get_status(**session_dict):
    cookies = {'sessionId': session_dict["cookie"]}
    r = session_dict['s'].get(session_dict['url'] + "file-transfer/status", cookies=cookies, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r
