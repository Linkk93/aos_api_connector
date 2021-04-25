from aos_s.aos_api_caller import AOSSwitchAPIClient
from aos_cx.aoscx_api_caller import AOSCXAPIClient
from cppm.cppm_api_caller import CPPMAPIClient
from example import common_ops
import json


def main_s():
    load_file = 'json_switchdata_s.json'
    with open(load_file, 'r') as f:
        data = json.load(f)
    aos_test = AOSSwitchAPIClient(**data)
    try:
        aos_test.connect()
        timesynch = aos_test.get_timesynch()
        print(timesynch)
    except Exception as e:
        print(e)
    aos_test.disconnect()


def main_cx():
    load_file = 'json_switchdata_cx.json'
    with open(load_file, 'r') as f:
        data = json.load(f)
    aocx_test = AOSCXAPIClient(**data)
    aocx_test.connect()
    sys_info = aocx_test.get_system_info()
    print(sys_info)
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


def create_radius_and_nd():
    # Switch Login Data
    switch_file = 'switch_list.csv'
    switchdata_list = common_ops.csv_to_dict(switch_file)
    # CPPM Login Data
    cppm_file = 'json_cppm_data_pw.json'
    # RADIUS Config to be pushed on CPPM and switches
    radius_file = 'json_radius_server.json'
    with open(radius_file, 'r') as f:
        radius_data = json.load(f)
    # generate shared secret if nothing is in JSON
    radius_data['secret'] = radius_data.get('secret', common_ops.generate_random(32))

    # Create CPPM connection
    with open(cppm_file, 'r') as f:
        cppm_data = json.load(f)
    cppm_client = CPPMAPIClient(**cppm_data)
    cppm_client.connect()
    for switch in switchdata_list:
        if switch["is_cx"].lower() == 'true':
            switch_client = AOSCXAPIClient(**switch)
        else:
            switch_client = AOSSwitchAPIClient(**switch)
        try:
            switch_client.connect()
            sys_info = switch_client.get_system_info()
            switch_client.new_radius_server(**radius_data)
            print(f'Created RADIUS Server {radius_data["address"]} on {sys_info["ip"]}\n')
            print(f'Creating ND on {radius_data["address"]}...\n')

            # create ND info dict
            nd_info = {
                "description": sys_info['hostname'],
                "name": sys_info['hostname'],
                "ip_address": sys_info['ip'],
                "radius_secret": radius_data['secret'],
                "tacacs_secret": radius_data['secret'],
                "vendor_name": "Aruba",
                "coa_capable": True,
                "coa_port": 3799
            }
            cppm_client.post_nd(nd_info)
            print(f'Created ND {sys_info["ip"]} on Server {radius_data["address"]}\n')
            print(f'Disconnecting from {sys_info["ip"]}...')
        except Exception as error:
            print(f'Error {error} \n disconnecting...')
        finally:
            switch_client.disconnect()
            print(f'Disconnected!\n')


def create_snmpv3():
    # Switch Login Data
    switch_file = 'json_switchdata_s.json'
    with open(switch_file, 'r') as f:
        sw = json.load(f)
    cl = AOSSwitchAPIClient(**sw)
    cl.connect()
    try:
        cl.enable_snmpv3()
        cl.new_snmpv3_user(username='api_user', auth_pw='auth_aruba123', priv_pw='priv_aruba123')
        cl.delete_snmpv3_user('initial')
    except Exception as e:
        print(e)
    cl.disconnect()


if __name__ == '__main__':
    main_s()
    # main_cx()
    # main_cppm()
    # create_radius_and_nd()
    # create_snmpv3()
