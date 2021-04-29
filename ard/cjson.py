import binascii
from .types import *

CompatibleJSONIntegerCode = '$ard.integer'
CompatibleJSONUIntegerCode = '$ard.uinteger'
CompatibleJSONBytesCode = '$ard.bytes'
CompatibleJSONMapCode = '$ard.map'

def to_cjson(value):
    value, _ = _to_cjson(value)
    return value

def _to_cjson(value):
    if isinstance(value, list):
        converted = False
        list_ = []
        for value_ in value:
            value_, valueConverted = _to_cjson(value_)
            if valueConverted:
                converted = True
            list_.append(value_)
        if converted:
            return list_, True

    if isinstance(value, tuple):
        converted = False
        list_ = []
        for value_ in value:
            value_, valueConverted = _to_cjson(value_)
            if valueConverted:
                converted = True
            list_.append(value_)
        if converted:
            return tuple(list_), True

    elif isinstance(value, dict):
        if len(value) == 1:
            # Check if we need escaping
            try:
                value_, _ = _to_cjson(value[CompatibleJSONIntegerCode])
                return {'$'+CompatibleJSONIntegerCode: value_}, True
            except KeyError:
                pass
            try:
                value_, _ = _to_cjson(value[CompatibleJSONUIntegerCode])
                return {'$'+CompatibleJSONUIntegerCode: value_}, True
            except KeyError:
                pass
            try:
                value_, _ = _to_cjson(value[CompatibleJSONBytesCode])
                return {'$'+CompatibleJSONBytesCode: value_}, True
            except KeyError:
                pass
            try:
                value_, _ = _to_cjson(value[CompatibleJSONMapCode])
                return {'$'+CompatibleJSONMapCode: value_}, True
            except KeyError:
                pass

        converted = False
        useList = False
        dict_ = {}
        list_ = []
        for key, value_ in value.items():
            value_, valueConverted = _to_cjson(value_)
            if valueConverted:
                converted = True
            if isinstance(key, str):
                list_.append({'key': key, 'value': value_})
                if not useList:
                    # We can stop building the dict_ if we switched to the list
                    dict_[key] = value_
            else:
                key, _ = _to_cjson(key)
                list_.append({'key': key, 'value': value_})
                useList = True
                converted = True
        if converted:
            if useList:
                return {CompatibleJSONMapCode: list_}, True
            else:
                return dict_, True

    elif isinstance(value, Map):
        list_ = []
        for key, value_ in value.items():
            key, _ = _to_cjson(key)
            value_, _ = _to_cjson(value_)
            list_.append({'key': key, 'value': value_})
        return {CompatibleJSONMapCode: list_}, True

    elif isinstance(value, UInteger): # must be before checking for 'int'
        return {CompatibleJSONUIntegerCode: str(value)}, True

    elif isinstance(value, int):
        return {CompatibleJSONIntegerCode: str(value)}, True

    elif isinstance(value, bytes):
        return {CompatibleJSONBytesCode: binascii.b2a_base64(value).decode()}, True

    return value, False

def from_cjson(value):
    value, _ = _from_cjson(value)
    return value

def _from_cjson(value):
    if isinstance(value, list):
        converted = False
        list_ = []
        for value_ in value:
            value_, valueConverted = _from_cjson(value_)
            if valueConverted:
                converted = True
            list_.append(value_)
        if converted:
            return list_, True

    elif isinstance(value, tuple):
        converted = False
        list_ = []
        for value_ in value:
            value_, valueConverted = _from_cjson(value_)
            if valueConverted:
                converted = True
            list_.append(value_)
        if converted:
            return tuple(list_), True

    elif isinstance(value, dict):
        if len(value) == 1:
            # Check for codes
            try:
                return int(value[CompatibleJSONIntegerCode]), True
            except KeyError:
                try:
                    return UInteger(value[CompatibleJSONUIntegerCode]), True
                except KeyError:
                    try:
                        return binascii.a2b_base64(value[CompatibleJSONBytesCode]), True
                    except KeyError:
                        try:
                            map_ = value[CompatibleJSONMapCode]
                            map__ = Map()
                            for entry in map_:
                                key, _ = _from_cjson(entry['key'])
                                value_, _ = _from_cjson(entry['value'])
                                map__[key] = value_
                            return map__.dict(), True
                        except KeyError:
                            # Handle escape code:
                            # $$ -> $
                            for key, value_ in value.items():
                                if key[:2] == '$$':
                                    key = key[1:]
                                    value_, _ = _from_cjson(value_)
                                    return {key: value_}, True

        converted = False
        map_ = Map()
        for key, value_ in value.items():
            key, keyConverted = _from_cjson(key)
            value_, valueConverted = _from_cjson(value_)
            if keyConverted or valueConverted:
                converted = True
            map_[key] = value_
        if converted:
            return map_.dict(), True

    return value, False
