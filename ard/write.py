
import ruamel.yaml, json, cbor2
from .types import *
from .yaml import represent_uinteger, represent_map
from .json import Encoder as JSONEncoder
from .cjson import convert_to as convert_to_cjson
from .cbor import encoder_default as cbor_encoder_default

__all__ = (
    'write',
    'write_yaml',
    'write_json',
    'write_cjson',
    'write_xml',
    'write_cbor')


def write(value, writer, format='yaml', indent='', strict=False):
    if (format == 'yaml') or (format == ''):
        write_yaml(value, writer, indent, strict)
    elif format == 'json':
        write_json(value, writer, indent)
    elif format == 'cjson':
        write_cjson(value, writer, indent)
    elif format == 'xml':
        write_xml(value, writer, indent)
    elif format == 'cbor':
        write_cbor(value, writer)
    else:
        raise Exception('unsupported format: ' + format)

def write_yaml(value, writer, indent='', strict=False):
    yaml=ruamel.yaml.YAML(typ='safe')
    yaml.indent = len(indent)
    yaml.representer.add_representer(UInteger, represent_uinteger)
    yaml.representer.add_representer(Map, represent_map)
    yaml.dump(value, writer)

def write_json(value, writer, indent=''):
    if indent == '':
        indent = None
    json.dump(value, writer, ensure_ascii=False, indent=indent, cls=JSONEncoder)
    writer.write('\n')

def write_cjson(value, writer, indent=''):
    value = convert_to_cjson(value)
    write_json(value, writer, indent)

def write_xml(value, writer, indent=''):
    # TODO
    raise NotImplementedError()

def write_cbor(value, writer):
    encoder = cbor2.CBOREncoder(writer, default=cbor_encoder_default)
    encoder.encode(value)
