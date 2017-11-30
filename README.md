# RIPE_STAT
Command Line tool and python module for extracting RIPE Statistics

## Installation
Run the setup.py using

`python setup.py install`

This sets up the module and one can use it as a module.

## Usage
the best use case is to call the script directly  with the necessary arguments

`python ripe_util.py -h`  gives the list of arguments supported 

## Return Value
According to the format parameter provided the script would print the output

### OUTPUT
The output is usually in the format
status => ok/nok , depending on whether the functionality was successful or not
data => list of items, where each item is the return message from the ripe API. 

## Usage as module
After importing the module the module function get_ripe_stat with the arguments

### Function parameters
1.) action [string] => one of 'network-info','geoloc' or 'as-overview'

2.) format [string] => one of 'json', 'xml' or 'yaml'

3.) ipaddr [list] => list of ip's as string , both ipv4 and ipv6

4.) asn_list [list] => list of ASN's as string, the format is plain numbers and no 'AS' prefixes

### Return Value
The output is the same as the return value of the script, but the only thing to note is that the output 
is a string-type. So the output has to converted into the respective native formats using the functions available.
Example: to get pure json data
`outputJson = json.loads(ripe_util.get_ripe_stat(ipaddr=['8.8.8.8']))`

## Requirements
Requires Python-3.6 or above
