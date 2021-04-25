# from cppm import xml_helper


def get_enf_profile(**session_dict):
    target_url = f"{session_dict['url']}config/read/EnforcementProfile/"
    r = session_dict['s'].get(target_url, auth=(session_dict['username'], session_dict['password']))
    if r.ok:
        return r
    else:
        print(f"HTTP Code: {r.status_code} \n  {r.reason} \n Message {r.text}")
        return r
