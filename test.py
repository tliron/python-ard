#!/usr/bin/env python3

import unittest, ard, json, sys, io


primitives = {
    'integer': 100,
    'uinteger': ard.UInteger(100),
    'float': 12.23,
    'bytes': b'\x7f\x45\x4c\x46\x01\x01\x01\x00',
    'escaped': {'$ard.integer': 'value'},
}

non_string_key = {
    100: 200,
}

unhashable_key = ard.Map([
    ('simple', 100),
    ({'complex': 'key'}, 200),
])

yaml_simple = '''
mylist:
- mymap:
    string: mystring
    integer: 100
    float: 12.34
'''

yaml_unhashable_key = '''
{complex: key}: value
'''

json_simple = '''
{"hello": "world"}
'''

cjson_simple = '''
{
  "$ard.map": [
    {
      "key": {"complex": "key"},
      "value": "value"
    }
  ]
}
'''


class Write(unittest.TestCase):
    def test_primitives(self):
        self._write(primitives)

    def test_unhashable_key(self):
        self._write(unhashable_key)

    def _write(self, data):
        print('YAML:')
        ard.write(data, sys.stdout)
        print('CJSON:')
        ard.write(data, sys.stdout, 'cjson')
        print('CBOR:')
        ard.write(data, sys.stdout.buffer, 'cbor')
        print()


class Code(unittest.TestCase):
    def test_yaml(self):
        self._roundtrip(unhashable_key, 'yaml')

    def test_cjson(self):
        self._roundtrip(unhashable_key, 'cjson')

    def test_cbor(self):
        self._roundtrip(unhashable_key, 'cbor')

    def _roundtrip(self, value, format):
        code = ard.encode(value, format)
        decoded = ard.decode(code, format)
        self.assertEqual(value, decoded)


class CJSON(unittest.TestCase):
    def test_primitives(self):
        self._roundtrip(primitives)

    def test_non_string_key(self):
        self._roundtrip(non_string_key)

    def test_unhashable_key(self):
        self._roundtrip(unhashable_key)

    def test_yaml(self):
        self._roundtrip(ard.decode(yaml_unhashable_key))

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
