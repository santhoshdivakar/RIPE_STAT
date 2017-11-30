"""
Module to test the output format of ripe_util Module.
Both positive and negative tests will be covered.
"""
import sys
import unittest
import json

sys.path.append('..')
import ripe_util

class TestStringMethods(unittest.TestCase):
    """
    To test the output format of the functions
    """
    def test_json_format(self):
        pass
    def test_xml_format(self):
        pass
    def test_yaml_format(self):
        pass

if __name__ == '__main__':
    unittest.main()