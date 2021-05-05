
import json
from .types import *

__all__ = ('Encoder',)


class Encoder(json.JSONEncoder):
    '''
    A JSONEncoder that supports the Map class.
    '''
    def default(self, obj):
        if isinstance(obj, Map):
            try:
                return obj.dict(strict=True, json=True)
            except TypeError:
                return obj._items
        return super().default(self, obj)
