import json


def get_timesynch(**session_dict):
    target_url = session_dict['url'] + "config/timesync"
    r = session_dict['s'].get(target_url, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r


def put_timesynch(sntp=False, timep=False, timep_or_sntp=True, ntp=False, **session_dict):
    # only one may be True
    if sntp and not (timep or timep_or_sntp or ntp):
        data = {'sntp': sntp}
    elif timep and not (sntp or timep_or_sntp or ntp):
        data = {'timep': timep}
    elif timep_or_sntp and not (sntp or timep or ntp):
        data = {'timep-or-sntp': timep_or_sntp}
    elif ntp and not (sntp or timep or timep_or_sntp):
        data = {'ntp': ntp}
    else:
        data = {}
    data = json.dumps(data)
    target_url = session_dict['url'] + "config/timesync"
    r = session_dict['s'].put(target_url, data=data, verify=False)
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
    return r
