
# aos_api_connector
API connector for ArubaOS products


## APIs supported:

* ArubaOS-S Switches
* ArubaOS-CX Switches
* Aruba ClearPass

## Installation
Install through [pypi]([https://pypi.org/project/aos-api-connector/](https://pypi.org/project/aos-api-connector/)) via pip:
````
pip install aos-api-connector
````
Or manually using the [GitHub]([https://github.com/Linkk93/aos_api_connector](https://github.com/Linkk93/aos_api_connector)).

## Usage

Every type of API has an API caller class. You can create instances of that class with at least three arguments:
* Username
* Password
* URL / IP / FQDN address of the device

After creating the device, use connect() to create a session. 
Then use the other functions to use the API. 
When you are finished use disconnect() to logout. 

### AurubaOS-S Switch
```
from aos_api_connector.aos_s import aos_api_caller as aos_s


data = { "url": "172.16.78.65",
  "username": "admin",
  "password": "Aruba123",
  "api_version": "v7"
}
switch = aos_s.AOSSwitchAPIClient(**data)
switch.connect()
sys_info = switch.get_system_info()
print(sys_info)
switch.disconnect()
```

### ArubaOS-CX
```
from aos_api_connector.aos_cx import aoscx_api_caller as aos_cx


data = { "url": "172.16.78.65",
  "username": "admin",
  "password": "Aruba123",
  "api_version": "v10.04"
}
switch = aos_cx.AOSCXwitchAPIClient(**data)
switch.connect()
sys_info = switch.get_system_info()
print(sys_info)
switch.disconnect()
```

### ClearPass
ClearPass neds either an API token or a username password.  That has to be set during instantiation of the API caller class.
You can choose with which you want to login, look into example folder for more info.

````
from  aos_api_connector.cppm import cppm_api_caller as cppm


data = {  
	"url": "10.10.10.10",  
	"api_version": "v1",  
	"client_id": "api_client",  
	"grant_type": "client_credentials",  
	"client_secret": "lTOcISWlXzDV3HCZLT8CVJlN9zxrUirdP+gHpva4mWZ5"  
	}
cppm_test = cppm.CPPMAPIClient(**data)
cppm_test.connect()  
nd_info = cppm_test.get_all_network_devices()  
for nd in nd_info['_embedded']['items']:  
    print(f"Name: {nd['name']} \nIP: {nd['ip_address']} \n\n")
````


#### Please note that there is no syntax check!
Some parameters are case sensitive. 
For example, api_version, there is no check for "V7" or "v7", but only "v7" will work.


### Differences between classes

The functions between the two classes should have the same name, if they end up doing the same. 
So both classes have connect(), disconnect() or get_vlans() even if they are implemented differently.

## Roadmap

I am working on implementing more functions and to create classes for the ClearPass and ArubaOS WLAN APIs.
After that I will create workflows spanning different APIs.
