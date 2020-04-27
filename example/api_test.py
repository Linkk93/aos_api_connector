from aos_s.aos_api_caller import AOSSwitchAPIClient
from aos_cx.aoscx_api_caller import AOSCXAPIClient
from cppm.cppm_api_caller import  CPPMAPIClient
import json


def main_s():
    load_file = 'switchdata_s.json'
    with open(load_file, 'r') as f:
        data = json.load(f)
    aos_test = AOSSwitchAPIClient(**data)
    aos_test.connect()
    vlan_info = aos_test.get_vlans()
    print(vlan_info)
    aos_test.disconnect()


def main_cx():
    load_file = 'switchdata_cx.json'
    with open(load_file, 'r') as f:
        data = json.load(f)
    aocx_test = AOSCXAPIClient(**data)
    aocx_test.connect()
    vlan_info = aocx_test.get_vlans()
    print(vlan_info)
    aocx_test.disconnect()


def main_cppm():
    load_file = 'json_cppm_data_pw.json'
    with open(load_file, 'r') as f:
        data = json.load(f)
    cppm_test = CPPMAPIClient(**data)
    cppm_test.connect()
    nd_info = cppm_test.get_all_network_devices()
    for nd in nd_info['_embedded']['items']:
        print(f"Name: {nd['name']} \nIP: {nd['ip_address']} \n\n")

    load_nd = 'json_nd_info.json'
    with open(load_nd, 'r') as f:
        nd_info = json.load(f)
    r = cppm_test.post_nd(nd_info)
    print(r)


if __name__ == '__main__':
    main_s()
    # main_cx()
