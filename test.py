#!/usr/bin/env python3

import unittest, ard, json, sys, io


data = {
    'string': 'mystring',
    'integer': 100,
    'uinteger': ard.UInteger(100),
    'float': 12.23,
    'bytes': b'\x7f\x45\x4c\x46\x01\x01\x01\x00',
    'escaped': {'$ard.integer': 'value'},
    'non-string-key': {1: 2},
    'complex-key': ard.Map((
        ('simple', 100),
        ({'complex': 'key'}, 200),
    )),
}

yaml_code = '''
string: mystring
integer: 100
float: 12.34
bytes: !!binary f0VMRgEBAQA=
escaped: {$ard.integer: value}
list-nesting:
- {complex: key1}: value
map-nesting:
  {complex: key2}: value
'''


class Write(unittest.TestCase):
    def test_yaml(self):
        ard.write(data, sys.stdout)
    
    def test_cjson(self):
        ard.write(data, sys.stdout, 'cjson')

    def test_cbor(self):
        ard.write(data, sys.stdout.buffer, 'cbor')


class Code(unittest.TestCase):
    def test_yaml(self):
        self._roundtrip(data, 'yaml')

    def test_cjson(self):
        self._roundtrip(data, 'cjson')

    def test_cbor(self):
        self._roundtrip(data, 'cbor')

    def _roundtrip(self, value, format):
        code = ard.encode(value, format)
        decoded = ard.decode(code, format)
        self.assertEqual(value, decoded)


class CJSON(unittest.TestCase):
    def test_data(self):
        self._roundtrip(data)

    def test_from_yaml(self):
        self._roundtrip(ard.decode(yaml_code))

    def _roundtrip(self, data):
        cjson = ard.cjson.convert_to(data)
        rt = ard.cjson.convert_from(cjson)

        print()
        print('Original:', data)
        print('CJSON: ', end='')
        json.dump(cjson, sys.stdout)
        print()

        self.assertEqual(data, rt)


if __name__ == '__main__':
    unittest.main()
