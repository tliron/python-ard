
import collections, cbor2
from .types import *

__all__ = (
  'encoder_default',
  'convert_frozendicts_to_maps')


def encoder_default(encoder, value):
  if isinstance(value, Map):
    return encoder.encode_map(value)
  raise cbor2.types.CBOREncodeTypeError('cannot serialize type ' + type(value).__name__)

def convert_frozendicts_to_maps(value):
  value, _ = _convert_frozendicts_to_maps(value)
  return value

def _convert_frozendicts_to_maps(value):
  if isinstance(value, list):
    converted = False
    list_ = []
    for value_ in value:
      value_, value_converted = _convert_frozendicts_to_maps(value_)
      if value_converted:
        converted = True
      list_.append(value_)
    if converted:
      return list_, True

  elif isinstance(value, tuple):
    converted = False
    list_ = []
    for value_ in value:
      value_, value_converted = _convert_frozendicts_to_maps(value_)
      if value_converted:
        converted = True
      list_.append(value_)
    if converted:
      return tuple(list_), True

  elif isinstance(value, collections.abc.Mapping):
    map_ = Map()
    converted = isinstance(value, cbor2.types.FrozenDict)
    for key in value:
      value_, value_converted = _convert_frozendicts_to_maps(value[key])
      key, key_converted = _convert_frozendicts_to_maps(key)
      map_[key] = value_
      if key_converted or value_converted:
        converted = True
    if converted:
      return map_.dict(), True

  return value, False
