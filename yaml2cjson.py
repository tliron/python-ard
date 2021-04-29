#!/usr/bin/env python3

import json, sys, cjson
from ruamel.yaml import YAML

yaml=YAML(typ='safe')
data = yaml.load('''
mylist:
- mymap:
    string: mystring
    integer: 100
    float: 12.34
''')

data = cjson.convert_to(data)

json.dump(data, sys.stdout, indent='  ')
print()
