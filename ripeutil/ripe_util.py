"""
Doc String
"""
import argparse
import re
import requests

SUPPORTED_FORMAT_TYPES = ['json', 'yaml', 'xml']
SUPPORTED_ACTION_TYPES = ['network-info', 'geoloc', 'as-overview']
SOFT_LIMIT_IGNORE = 'soft_limit=ignore'
ACTION_PARAM_MAP = {'network-info' : ['ip'], 'geoloc' : ['ip', 'asn'], 'as-overview' : ['asn'] }

def checkIpType(ip):
    if re.match("""^(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}$""",ip):
        return 'ipv4'
    #if re.match("""(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])(\/\d{1,3})?)""", ip):
    #    return 'ipv6'
    #Check for the IPV6 before 
    return 'none'

def getRipeStat(action='network-info', format='json', ipaddr=[], asn_list=[]):
    stat = {}
    # validate inputs
    if format not in SUPPORTED_FORMAT_TYPES:
        return {'status':'nok', 'error':'invalid output format'}
    pass
    if action not in SUPPORTED_ACTION_TYPES:
        return {'status':'nok', 'error':'invalid action'}
    pass

    param_list = []
    if 'ip' in ACTION_PARAM_MAP[action]:
        for ip in ipaddr:
            if checkIpType(ip) == 'none':
                return {'status':'nok', 'error':'invalid IP %s'%(ip,)}
            else:
                param_list.append(ip)
            pass
        pass
    pass
    if 'ip' in ACTION_PARAM_MAP[action]:
        for asn in asn_list:
            if invalidASN(asn):
                return {'status':'nok', 'error':'invalid ASN %s'%(asn,)}
            else:
                param_list.append(asn)
            pass
        pass
    pass
    if len(param_list) == 0:
        return {'status':'nok', 'error':'no valid parameters provided for the action'}
    pass

    # Form the URL parameters and call the service. 
    url = 'https://stat.ripe.net/data/%s/data.json?resource='%(action,)

    # Call the service.since any input has the same key, we use a single param_list
    for input_param in param_list:
        r = requests.get(url+input_param)
        if r.status_code == 200:
            print("SUCCESS", r.json())
        pass
    pass
    # Parse the reply to the format we need
    return stat

def main():
    my_parser = argparse.ArgumentParser(description='RIPE Statistics Tool')
    my_parser.add_argument(
        '-a','--action', type=str, 
        choices=SUPPORTED_ACTION_TYPES, 
        default='network-info')
    my_parser.add_argument('-i','--ipaddr', type=str, action='append', default=[])
    my_parser.add_argument('--asn', type=str, action='append', default=[])
    my_parser.add_argument('-f','--format', type=str, choices=SUPPORTED_FORMAT_TYPES, default='json')
    arg_list = vars(my_parser.parse_args())
    print(getRipeStat(action=arg_list['action'], ipaddr=arg_list['ipaddr'], \
                      format=arg_list['format'], asn_list=arg_list['asn']))


if __name__ == '__main__':
    main()

