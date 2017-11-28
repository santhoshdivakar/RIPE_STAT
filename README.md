# RIPE_STAT
Command Line tool for extracting RIPE Statistics

## Installation
Run the setup.py using

`python setup.py install`

This sets up the module and one can use it as a module.

## Usage
the best use case is to call the script directly  with the necessary arguments

`python ripe_util.py -h`  gives the list of arguments supported 

## Usage as module
After importing the module the module function get_ripe_stat with the arguments

### Function parameters
1.) action [string] => one of 'network-info','geoloc' or 'as-overview'

2.) format [string] => one of 'json', 'xml' or 'yaml'

3.) ipaddr [list] => list of ip's as string , both ipv4 and ipv6

4.) asn_list [list] => list of ASN's as string, the format is plain numbers and no 'AS' prefixes


## Requirements
Requires Python-3.6 or above
