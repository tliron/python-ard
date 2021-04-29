#!/usr/bin/env python3

import json, sys, ard
from ruamel.yaml import YAML
yaml=YAML(typ='safe')

def show(data):
    print('Original:', data)

    cjson = ard.to_cjson(data)
    print('CJSON:')
    json.dump(cjson, sys.stdout, indent='  ')
    print()

    rt = ard.from_cjson(cjson)
    print('Roundtrip:', 'success' if data == rt else 'failure', rt)

# Primitives
show({
    'integer': 100,
    'uinteger': ard.UInteger(100),
    'float': 12.23,
    'bytes': b'\x7f\x45\x4c\x46\x01\x01\x01\x00',
    'escaped': {'$ard.integer': 'value'},
})

# Dict with a non-string key
show({
    100: 200,
})

# Dict with an unhashable key
show(ard.Map([
    ({'complex': 'key'}, 200),
]))

# YAML
show(yaml.load('''
mylist:
- mymap:
    string: mystring
    integer: 100
    float: 12.34
'''))

# YAML with an unhashable key
#show(yaml.load('''
#{complex: key}: value
#'''))
