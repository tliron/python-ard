
import io, binascii
from .read import *
from .exceptions import *

__all__ = (
  'decode',
  'decode_yaml',
  'decode_json',
  'decode_cjson',
  'decode_xml',
  'decode_cbor')


def decode(code, format='yaml'):
  if (format == 'yaml') or (format == ''):
    return decode_yaml(code)
  elif format == 'json':
    return decode_json(code)
  elif format == 'cjson':
    return decode_cjson(code)
  elif format == 'xml':
    return decode_xml(code)
  elif format == 'cbor':
    return decode_cbor(code)
  else:
    raise ARDException('unsupported format: ' + format)

def decode_yaml(code):
  return read_yaml(io.StringIO(code))

def decode_json(code):
  return read_json(io.StringIO(code))

def decode_cjson(code):
  return read_cjson(io.StringIO(code))

def decode_xml(code):
  return read_xml(io.StringIO(code))

def decode_cbor(code):
  bytes_ = binascii.a2b_base64(code)
  return read_cbor(io.BytesIO(bytes_))
