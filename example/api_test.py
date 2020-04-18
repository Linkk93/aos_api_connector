from aos_api_caller import AOSSwitchAPIClient
from aoscx_api_caller import AOSCXAPIClient
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


if __name__ == '__main__':
    main_s()
    # main_cx()
