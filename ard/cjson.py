
import collections, binascii
from .types import *

__all__ = (
    'CJSON_INTEGER_CODE',
    'CJSON_UINTEGER_CODE',
    'CJSON_BYTES_CODE',
    'CJSON_MAP_CODE',
    'convert_to',
    'convert_from')

CJSON_INTEGER_CODE = '$ard.integer'
CJSON_UINTEGER_CODE = '$ard.uinteger'
CJSON_BYTES_CODE = '$ard.bytes'
CJSON_MAP_CODE = '$ard.map'


def convert_to(value):
    value, _ = _convert_to(value)
    return value

def _convert_to(value):
    if isinstance(value, list):
        converted = False
        list_ = []
        for value_ in value:
            value_, value_converted = _convert_to(value_)
            if value_converted:
                converted = True
            list_.append(value_)
        if converted:
            return list_, True

    elif isinstance(value, tuple):
        converted = False
        list_ = []
        for value_ in value:
            value_, value_converted = _convert_to(value_)
            if value_converted:
                converted = True
            list_.append(value_)
        if converted:
            return tuple(list_), True

    elif isinstance(value, collections.abc.Mapping):
        if len(value) == 1:
            # Check if we need escaping
            try:
                value_, _ = _convert_to(value[CJSON_INTEGER_CODE])
                return {'$'+CJSON_INTEGER_CODE: value_}, True
            except KeyError:
                pass
            try:
                value_, _ = _convert_to(value[CJSON_UINTEGER_CODE])
                return {'$'+CJSON_UINTEGER_CODE: value_}, True
            except KeyError:
                pass
            try:
                value_, _ = _convert_to(value[CJSON_BYTES_CODE])
                return {'$'+CJSON_BYTES_CODE: value_}, True
            except KeyError:
                pass
            try:
                value_, _ = _convert_to(value[CJSON_MAP_CODE])
                return {'$'+CJSON_MAP_CODE: value_}, True
            except KeyError:
                pass

        converted = False
        use_list = False
        dict_ = {}
        list_ = []
        for key in value:
            value_, value_converted = _convert_to(value[key])
            if value_converted:
                converted = True
            if isinstance(key, str):
                list_.append({'key': key, 'value': value_})
                if not use_list:
                    # We can stop building the dict_ if we switched to the list
                    dict_[key] = value_
            else:
                key, _ = _convert_to(key)
                list_.append({'key': key, 'value': value_})
                use_list = True
                converted = True
        if converted:
            if use_list:
                return {CJSON_MAP_CODE: list_}, True
            else:
                return dict_, True
        elif isinstance(value, Map):
            # Maps are not JSON-serializable, so we need the conversion
            return dict_, True

    elif isinstance(value, UInteger): # must be before checking for 'int'
        return {CJSON_UINTEGER_CODE: str(value)}, True

    elif isinstance(value, int):
        return {CJSON_INTEGER_CODE: str(value)}, True

    elif isinstance(value, bytes):
        return {CJSON_BYTES_CODE: binascii.b2a_base64(value).decode()}, True

    return value, False

def convert_from(value):
    value, _ = _convert_from(value)
    return value

def _convert_from(value):
    if isinstance(value, list):
        converted = False
        list_ = []
        for value_ in value:
            value_, value_converted = _convert_from(value_)
            if value_converted:
                converted = True
            list_.append(value_)
        if converted:
            return list_, True

    elif isinstance(value, tuple):
        converted = False
        list_ = []
        for value_ in value:
            value_, value_converted = _convert_from(value_)
            if value_converted:
                converted = True
            list_.append(value_)
        if converted:
            return tuple(list_), True

    elif isinstance(value, collections.abc.Mapping):
        if len(value) == 1:
            # Check for codes
            try:
                return int(value[CJSON_INTEGER_CODE]), True
            except KeyError:
                try:
                    return UInteger(value[CJSON_UINTEGER_CODE]), True
                except KeyError:
                    try:
                        return binascii.a2b_base64(value[CJSON_BYTES_CODE]), True
                    except KeyError:
                        try:
                            map_ = value[CJSON_MAP_CODE]
                            map__ = Map()
                            for entry in map_:
                                key, _ = _convert_from(entry['key'])
                                value_, _ = _convert_from(entry['value'])
                                map__[key] = value_
                            return map__.dict(), True
                        except KeyError:
                            # Handle escape code:
                            # $$ -> $
                            for key, value_ in value.items():
                                if key[:2] == '$$':
                                    key = key[1:]
                                    value_, _ = _convert_from(value_)
                                    return {key: value_}, True

        converted = False
        map_ = Map()
        for key, value_ in value.items():
            key, key_converted = _convert_from(key)
            value_, value_converted = _convert_from(value_)
            if key_converted or value_converted:
                converted = True
            map_[key] = value_
        if converted:
            return map_.dict(), True

    return value, False
