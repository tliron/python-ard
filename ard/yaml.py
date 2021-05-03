
import ruamel.yaml
from .types import *

__all__ = (
    'SafeConstructor',
    'represent_uinteger')


class SafeConstructor(ruamel.yaml.constructor.SafeConstructor):
    '''
    A SafeConstructor that uses the Map class, allowing it to support YAML maps with complex keys.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yaml_base_dict_type = Map


class Constructor(ruamel.yaml.constructor.Constructor):
    '''
    A Constructor that uses the Map class, allowing it to support YAML maps with complex keys.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yaml_base_dict_type = Map


class RoundTripConstructor(ruamel.yaml.constructor.RoundTripConstructor):
    '''
    A RoundTripConstructor that uses the Map class, allowing it to support YAML maps with complex keys.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yaml_base_dict_type = Map


def represent_uinteger(representer, data):
    return representer.represent_int(data)

def represent_map(representer, data):
    return representer.represent_dict(data)
