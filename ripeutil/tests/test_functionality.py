"""
Module to test the functionality of ripe_util Module.
Both positive and negative tests will be covered.
"""
import sys
import unittest
import json

sys.path.append('..')
import ripe_util

class TestStringMethods(unittest.TestCase):
    """
    To test the validation of the inputs
    """
    def test_network_info(self):
        #ipv4
        output = ripe_util.get_ripe_stat(action='network-info', fmt='json',ipaddr=['49.44.97.154'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        #ipv6
        output = ripe_util.get_ripe_stat(action='network-info', fmt='json',ipaddr=['2001:4860:4860::8844'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        #ipv4+ipv6
        output = ripe_util.get_ripe_stat(action='network-info', fmt='json',ipaddr=['8.8.8.8','2001:4860:4860::8844'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        reply = output["data"][1]
        self.assertEqual(reply['status'],'ok')
        pass
    def test_as_overview(self):
        pass
    def test_geoloc(self):
        pass

if __name__ == '__main__':
    unittest.main()
