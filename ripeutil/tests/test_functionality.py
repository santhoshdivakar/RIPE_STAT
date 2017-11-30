"""
Module to test the functionality of ripeutil.ripe_util Module.
Both positive and negative tests will be covered.
"""
import sys
import unittest
import json

sys.path.append('..')
import ripeutil

class TestStringMethods(unittest.TestCase):
    """
    To test the validation of the inputs
    """
    def test_network_info(self):
        #ipv4
        output = ripeutil.ripe_util.get_ripe_stat(action='network-info', fmt='json',ipaddr=['49.44.97.154'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        #ipv6
        output = ripeutil.ripe_util.get_ripe_stat(action='network-info', fmt='json',ipaddr=['2001:4860:4860::8844'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        #ipv4+ipv6
        output = ripeutil.ripe_util.get_ripe_stat(action='network-info', fmt='json',ipaddr=['8.8.8.8','2001:4860:4860::8844'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        reply = output["data"][1]
        self.assertEqual(reply['status'],'ok')
        # asn only
        output = ripeutil.ripe_util.get_ripe_stat(action='network-info', fmt='json',asn_list=['8844'])
        output = json.loads(output)
        self.assertEqual(output['status'],'nok')
        pass
    def test_as_overview(self):
        # asn only
        output = ripeutil.ripe_util.get_ripe_stat(action='as-overview', fmt='json',asn_list=['8844'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        # 2 asn + ipv4
        output = ripeutil.ripe_util.get_ripe_stat(action='as-overview', fmt='json',asn_list=['8844','55386'], ipaddr=['8.8.8.8'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        reply = output["data"][1]
        self.assertEqual(reply['status'],'ok')
        length_of_reply = len(output["data"])
        self.assertEqual(length_of_reply, 2)
        #ipv6
        output = ripeutil.ripe_util.get_ripe_stat(action='as-overview', fmt='json',ipaddr=['2001:4860:4860::8844'])
        output = json.loads(output)
        self.assertEqual(output['status'],'nok')
        pass
    def test_geoloc(self):
        # 2 asn + ipv4
        output = ripeutil.ripe_util.get_ripe_stat(action='geoloc', fmt='json',asn_list=['8844','55386'], ipaddr=['8.8.8.8'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        reply = output["data"][1]
        self.assertEqual(reply['status'],'ok')
        reply = output["data"][2]
        self.assertEqual(reply['status'],'ok')
        length_of_reply = len(output["data"])
        self.assertEqual(length_of_reply, 3)
        #  ipv4
        output = ripeutil.ripe_util.get_ripe_stat(action='geoloc', fmt='json',ipaddr=['8.8.8.8'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        length_of_reply = len(output["data"])
        self.assertEqual(length_of_reply, 1)
        #ipv6
        output = ripeutil.ripe_util.get_ripe_stat(action='geoloc', fmt='json',ipaddr=['2001:4860:4860::8844'])
        output = json.loads(output)
        reply = output["data"][0]
        self.assertEqual(reply['status'],'ok')
        length_of_reply = len(output["data"])
        self.assertEqual(length_of_reply, 1)
        #no-inputs
        output = ripeutil.ripe_util.get_ripe_stat(action='geoloc', fmt='json')
        output = json.loads(output)
        self.assertEqual(output['status'],'nok')
        pass

if __name__ == '__main__':
    unittest.main()
