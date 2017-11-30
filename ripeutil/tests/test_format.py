"""
Module to test the output format of ripe_util Module.
Both positive and negative tests will be covered.
"""
import sys
import unittest
import json
import yaml
import xml.etree.ElementTree as ET

sys.path.append('..')
from ripeutil import ripe_util

class TestStringMethods(unittest.TestCase):
    """
    To test the output format of the functions
    """
    def test_json_format(self):
        output = ripe_util.get_ripe_stat(action='geoloc', fmt='json',ipaddr=['2001:4860:4860::8844'])
        output = json.loads(output)
        self.assertTrue('status' in output.keys())
        pass
    def test_xml_format(self):
        output = ripe_util.get_ripe_stat(action='geoloc', fmt='xml',ipaddr=['2001:4860:4860::8844'])
        root = ET.fromstring(output)
        self.assertTrue(root[0].tag == 'status')
        pass
    def test_yaml_format(self):
        output = ripe_util.get_ripe_stat(action='geoloc', fmt='yaml',ipaddr=['2001:4860:4860::8844'])
        output = yaml.load(output)
        self.assertTrue('status' in output.keys())
        pass

if __name__ == '__main__':
    unittest.main()