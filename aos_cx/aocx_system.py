import os
import json


def get_temperature(attributes='temp_sensors', depth=3, **sesion_dict):
    target_url = sesion_dict["url"] + f"system/subsystems/management_module,1%2F1?attributes={attributes}&depth={depth}"
    r = sesion_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_subsystem_info(attributes='product_info,power_supplies,boot_time', ss_type='chassis,1', depth=3, **sesion_dict):
    target_url = sesion_dict["url"] + f"system/subsystems/{ss_type}?attributes={attributes}&depth={depth}"
    r = sesion_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_systeminfo(attributes='hostname,software_version,mgmt_intf,system_mac', depth=0, **sesion_dict):
    target_url = sesion_dict["url"] + "system?attributes={}&depth={}".format(attributes, depth)
    r = sesion_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def get_system_info_all(**session_dict):
    system_info = get_systeminfo(**session_dict)
    sub_info = get_subsystem_info(**session_dict)
    merged_info = {**system_info, **sub_info['product_info'], 'boot_time': sub_info['boot_time']}
    return merged_info


def get_version(**session_dict):
    target_url = session_dict["url"] + "firmware"
    r = session_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def upgrade(firmware: str, partition: str = 'primary', **session_dict):
    if os.path.isfile(firmware) and os.path.exists(firmware):
        target_url = session_dict["url"] + f'firmware?image={partition}'

        firmware = os.path.abspath(firmware)

        files = json.dumps({'file': open(firmware, 'rb')})

        headers = {
            'Accept': '*/*'
        }

        r = session_dict['s'].post(target_url, files=files, headers=headers, verify=False)

        if r.ok:
            return r.json()
        else:
            print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
            return {}
    else:
        print('incorrect path to firmware')
        return {}


def get_config(configname, **session_dict):
    target_url = session_dict["url"] + "fullconfigs/{}".format(configname)
    r = session_dict["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}


def put_config(config_path, config_name, **session_dict):
    target_url = session_dict["url"] + "fullconfigs/{}".format(config_name)
    with open(config_path, 'r') as f:
        r = session_dict["s"].put(target_url, verify=False, json=json.load(f))
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
