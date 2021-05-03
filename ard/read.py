
import ruamel.yaml, json, cbor2
from .yaml import SafeConstructor as YAMLSafeConstructor
from .json import Encoder as JSONEncoder
from .cjson import convert_from as convert_from_cjson
from .cbor import convert_frozendicts_to_maps

__all__ = (
    'read',
    'read_yaml',
    'read_json',
    'read_cjson',
    'read_cbor')


def read(reader, format='yaml'):
    if (format == 'yaml') or (format == ''):
        return read_yaml(reader)
    elif format == 'json':
        return read_json(reader)
    elif format == 'cjson':
        return read_cjson(reader)
    elif format == 'cbor':
        return read_cbor(reader)
    else:
        raise Exception('unsupported format: ' + format)

def read_yaml(reader):
    yaml=ruamel.yaml.YAML(typ='safe')
    yaml.Constructor = YAMLSafeConstructor
    return yaml.load(reader)

def read_json(reader):
    return json.load(reader)

def read_cjson(reader):
    cjson = read_json(reader)
    return convert_from_cjson(cjson)

def read_cbor(reader):
    decoder = cbor2.CBORDecoder(reader)
    return convert_frozendicts_to_maps(decoder.decode())
