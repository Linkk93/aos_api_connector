# aos_api_connector
API connector for ArubaOS products


## APIs supported:

* ArubaOS-S Switches
* ArubaOS-CX Switches
* Aruba ClearPass


## Usage

Every type of API has an API caller class. You can create instances of that class with at least three arguments:
* Username
* Password
* URL / IP / FQDN address of the device
```
data = { "url": "172.16.78.65",
  "username": "admin",
  "password": "Aruba123",
  "api_version": "v10.04"
}
aocx_test = AOSCXAPIClient(**data)
```

After creating the device, use connect() to create a session. 
Then use the other functions to use the API. 
When you are finished use disconnect() to logout. 

#### Please note that there is no syntax check!
Some parameters are case sensitive. 
For example, api_version, there is no check for "V7" or "v7", but only "v7" will work.

### Examples
Examples can be found in the example folder.

### Differences between classes

The functions between the two classes should have the same name, if they end up doing the same. 
So both classes have connect(), disconnect() or get_vlans() even if they are implemented differently.

## Roadmap

I am working on implementing more functions and to create classes for the ClearPass and ArubaOS WLAN APIs.
After that I will create workflows spanning different APIs.
