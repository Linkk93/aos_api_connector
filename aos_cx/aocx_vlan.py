

def get_vlans(attributes='description,admin,oper_state,type,name,id,voice', depth=3, **kwargs):
    target_url = kwargs["url"] + "system/vlans?attributes={}&depth={}".format(attributes, depth)
    r = kwargs["s"].get(target_url, verify=False)
    if r.ok:
        return r.json()
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return {}
