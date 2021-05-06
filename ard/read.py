
import ruamel.yaml, json, cbor2
from .exceptions import *
from .yaml import SafeConstructor as YAMLSafeConstructor
from .json import Encoder as JSONEncoder
from .cjson import convert_from as convert_from_cjson
from .cbor import convert_frozendicts_to_maps

__all__ = (
    'read',
    'read_yaml',
    'read_json',
    'read_cjson',
    'read_xml',
    'read_cbor')


def read(stream, format='yaml'):
    if (format == 'yaml') or (format == ''):
        return read_yaml(stream)
    elif format == 'json':
        return read_json(stream)
    elif format == 'cjson':
        return read_cjson(stream)
    elif format == 'xml':
        return read_xml(stream)
    elif format == 'cbor':
        return read_cbor(stream)
    else:
        raise ARDException('unsupported format: ' + format)

def read_yaml(stream):
    try:
        yaml=ruamel.yaml.YAML(typ='safe')
        yaml.Constructor = YAMLSafeConstructor
        return yaml.load(stream)
    except Exception as e:
        raise DecodeError('yaml') from e

def read_json(stream):
    try:
        return json.load(stream)
    except Exception as e:
        raise DecodeError('json') from e

def read_cjson(stream):
    cjson = read_json(stream)
    try:
        return convert_from_cjson(cjson)
    except Exception as e:
        raise DecodeError('cjson') from e

def read_xml(stream):
    # TODO
    raise NotImplementedError('xml')

def read_cbor(stream):
    try:
        decoder = cbor2.CBORDecoder(stream)
        return convert_frozendicts_to_maps(decoder.decode())
    except Exception as e:
        raise DecodeError('cbor') from e
