"""
Doc String
"""
import argparse
import re
import json
import yaml
import requests
import dicttoxml

SUPPORTED_FORMAT_TYPES = ['json', 'yaml', 'xml']
SUPPORTED_ACTION_TYPES = ['network-info', 'geoloc', 'as-overview']
SOFT_LIMIT_IGNORE = 'soft_limit=ignore'
ACTION_PARAM_MAP = {'network-info' : ['ip'], 'geoloc' : ['ip', 'asn'], 'as-overview' : ['asn']}

def _check_ip_type(ip_addr):
    if re.match("""^(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}$""", ip_addr): #pylint: disable=C0301
        return 'ipv4'
    #if re.match("""(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])(\/\d{1,3})?)""", ip): #pylint: disable=C0301
    #    return 'ipv6'
    #Check for the IPV6 before
    return 'none'

def _invalid_asn(asn):
    """
    Checks if the given string is a proper ASN.
    """
    if re.match("\d+", asn):
        return False
    return True

def _result_format(fmt, data):
    """
    The function converts the given data into the format required.abs
    The allowed formats are json, xml and yaml.
    """
    if fmt == 'json':
        return json.dumps(data)
    if fmt == 'xml':
        return dicttoxml.dicttoxml(data)
    if fmt == 'yaml':
        return yaml.dump(data)
    return data

def _validate_inputs(action, fmt, ip_addr_list, asn_list):
    if fmt not in SUPPORTED_FORMAT_TYPES:
        return {'status':'nok', 'error':'invalid output format'}
    if action not in SUPPORTED_ACTION_TYPES:
        return {'status':'nok', 'error':'invalid action'}

    param_list = []
    if 'ip' in ACTION_PARAM_MAP[action]:
        for ip_addr in ip_addr_list:
            if _check_ip_type(ip_addr) == 'none':
                return {'status':'nok', 'error':'invalid IP %s'%(ip_addr,)}
            else:
                param_list.append(ip_addr)
            pass
        pass
    pass
    if 'asn' in ACTION_PARAM_MAP[action]:
        for asn in asn_list:
            if _invalid_asn(asn):
                return {'status':'nok', 'error':'invalid ASN %s'%(asn,)}
            else:
                param_list.append(asn)
            pass
        pass
    pass
    if not param_list:
        return {'status':'nok', 'error':'no valid parameters provided for the action'}

    return {'status':'ok', 'data': param_list}

def get_ripe_stat(action='network-info', fmt='json', ipaddr=[], asn_list=[]):
    """
    The main function of the ripe_util.py.
    This will query the RIPE API to find the required information and
    pass it back to the user in the desired format
    """
    # validate inputs
    validate_inputs = _validate_inputs(action, fmt, ipaddr, asn_list)
    if validate_inputs['status'] != 'ok':
        return _result_format(fmt, validate_inputs)
    else:
        param_list = validate_inputs['data']

    # Form the URL parameters and call the service.
    url = 'https://stat.ripe.net/data/%s/data.json?resource='%(action,)

    # Call the service.since any input has the same key, we use a single param_list
    data = []
    for input_param in param_list:
        response = requests.get(url+input_param)
        if response.status_code == 200:
            #print("SUCCESS", format, r.json())
            data.append(response.json())
        else:
            data.append({'status':'nok', 'error':'finding data for %s unsuccessful'%(input_param,)})
        pass
    pass
    # Parse the reply to the format we need
    return _result_format(fmt, {'status':'ok', 'data':data})

def _main():
    """
    The Main function to be called when the module is invoked as command line
    """
    my_parser = argparse.ArgumentParser(description='RIPE Statistics Tool')
    my_parser.add_argument(
        '-a', '--action', type=str,
        choices=SUPPORTED_ACTION_TYPES,
        default='network-info')
    my_parser.add_argument('-i', '--ipaddr', type=str, action='append', default=[])
    my_parser.add_argument('--asn', type=str, action='append', default=[])
    my_parser.add_argument('-f', '--format', type=str, choices=SUPPORTED_FORMAT_TYPES, default='json') #pylint: disable=C0301
    arg_list = vars(my_parser.parse_args())
    print(get_ripe_stat(action=arg_list['action'], ipaddr=arg_list['ipaddr'], \
                      fmt=arg_list['format'], asn_list=arg_list['asn']))


if __name__ == '__main__':
    _main()

