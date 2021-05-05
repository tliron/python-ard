
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


def read(reader, format='yaml'):
    if (format == 'yaml') or (format == ''):
        return read_yaml(reader)
    elif format == 'json':
        return read_json(reader)
    elif format == 'cjson':
        return read_cjson(reader)
    elif format == 'xml':
        return read_xml(reader)
    elif format == 'cbor':
        return read_cbor(reader)
    else:
        raise ARDException('unsupported format: ' + format)

def read_yaml(reader):
    try:
        yaml=ruamel.yaml.YAML(typ='safe')
        yaml.Constructor = YAMLSafeConstructor
        return yaml.load(reader)
    except Exception as e:
        raise DecodeError('yaml') from e

def read_json(reader):
    try:
        return json.load(reader)
    except Exception as e:
        raise DecodeError('json') from e

def read_cjson(reader):
    cjson = read_json(reader)
    try:
        return convert_from_cjson(cjson)
    except Exception as e:
        raise DecodeError('cjson') from e

def read_xml(reader):
    # TODO
    raise NotImplementedError()

def read_cbor(reader):
    try:
        decoder = cbor2.CBORDecoder(reader)
        return convert_frozendicts_to_maps(decoder.decode())
    except Exception as e:
        raise DecodeError('cbor') from e
