
import io, binascii
from .write import *

__all__ = (
    'encode',
    'encode_yaml',
    'encode_json',
    'encode_cjson',
    'encode_cbor')


def encode(value, format='yaml', indent='', strict=False):
    if (format == 'yaml') or (format == ''):
        return encode_yaml(value, indent, strict)
    elif format == 'json':
        return encode_json(value, indent)
    elif format == 'cjson':
        return encode_cjson(value)
    elif format == 'cbor':
        return encode_cbor(value)
    else:
        raise Exception('unsupported format: ' + format)

def encode_yaml(value, indent='', strict=False):
    buffer = io.StringIO()
    write_yaml(value, buffer, indent, strict)
    return buffer.getvalue()

def encode_json(value, indent=''):
    buffer = io.StringIO()
    write_json(value, buffer, indent)
    return buffer.getvalue()

def encode_cjson(value, indent=''):
    buffer = io.StringIO()
    write_cjson(value, buffer, indent)
    return buffer.getvalue()

def encode_cbor(value):
    buffer = io.BytesIO()
    write_cbor(value, buffer)
    return binascii.b2a_base64(buffer.getvalue()).decode()
