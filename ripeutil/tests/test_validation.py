"""
Module to test the validation of ripe_util.
Both positive and negative tests will be covered.
"""
import sys
import unittest

sys.path.append('..')
import ripe_util

class TestStringMethods(unittest.TestCase):
    """
    To test the validation of the inputs
    """
    def test_asn_validation(self):
        result = ripe_util._validate_inputs('as-overview', 'json', [], ['2345'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('as-overview', 'json', [], ['Helloworld'])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('as-overview', 'json', [], ['AS2345'])
        self.assertEqual(result['status'],'nok')
        return

    def test_ip_validation(self):
        result = ripe_util._validate_inputs('geoloc', 'json', ['8.8.8.8'], [])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('geoloc', 'json', ['100.100.1.2'], [])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('geoloc', 'json', ['800.900.10.10'], [])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('geoloc', 'json', ['1.2.3.888'], [])
        self.assertEqual(result['status'],'nok')
        return
    
    def test_action_validation(self):
        result = ripe_util._validate_inputs('geoloc', 'json', ['8.8.8.8'], ['2345'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('geoloc', 'json', ['8.8.8.8','1.2.3.4'], [])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('geoloc', 'json', [], [])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('geoloc', 'json', ['8.8.8.8','2001:db8:85a3:8d3:1319:8a2e:370:7348'], [])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('geoloc', 'json', ['8.8.8.8','2001:db8:85a3:8d3:1319:8a2e:370'], [])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('as-overview', 'json', ['8.8.8.8'], ['2345'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('as-overview', 'json', ['8.8.8.8','1.2.3.4'], [])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('as-overview', 'json', [], ['2345','1000'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('as-overview', 'json', [], [])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('network-info', 'json', ['8.8.8.8'], ['2345'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('network-info', 'json', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('network-info', 'json', ['8.8.8.8','1.2.3.4'], [])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('network-info', 'json', [], [])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('blahblah', 'json', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('network-information', 'json', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'nok')
        pass
    
    def test_format_validation(self):
        result = ripe_util._validate_inputs('network-info', 'json', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('network-info', 'xml', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('network-info', 'yaml', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'ok')
        result = ripe_util._validate_inputs('network-info', 'jsonp', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'nok')
        result = ripe_util._validate_inputs('network-info', 'md', ['8.8.8.8'], ['2345','5566'])
        self.assertEqual(result['status'],'nok')
        pass


if __name__ == '__main__':
    unittest.main()
