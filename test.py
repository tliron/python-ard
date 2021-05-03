#!/usr/bin/env python3

import unittest, json, sys, ard
from ruamel.yaml import YAML
yaml=YAML(typ='safe')

class TestCJSON(unittest.TestCase):
    def test_primitives(self):
        self.roundtrip({
            'integer': 100,
            'uinteger': ard.UInteger(100),
            'float': 12.23,
            'bytes': b'\x7f\x45\x4c\x46\x01\x01\x01\x00',
            'escaped': {'$ard.integer': 'value'},
        })

    def test_non_string_key(self):
        self.roundtrip({
            100: 200,
        })

    def test_unhashable_key(self):
        self.roundtrip(ard.Map([
            ('simple', 100),
            ({'complex': 'key'}, 200),
        ]))

    def test_yaml(self):
        self.roundtrip(yaml.load('''
        mylist:
        - mymap:
            string: mystring
            integer: 100
            float: 12.34
        '''))

    def _test_yaml_unhashable_key(self):
        self.roundtrip(yaml.load('''
        {complex: key}: value
        '''))

    def roundtrip(self, data):
        cjson = ard.to_cjson(data)
        rt = ard.from_cjson(cjson)

        print()
        print('Original:', data)
        print('CJSON: ', end='')
        json.dump(cjson, sys.stdout)
        print()

        self.assertEqual(data, rt)


if __name__ == '__main__':
    unittest.main()
