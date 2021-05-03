
import json
from .types import *

class Encoder(json.JSONEncoder):
    '''
    A JSONEncoder that supports the Map class.
    '''
    def default(self, obj):
        if isinstance(obj, Map):
            return obj.entries
        return json.JSONEncoder.default(self, obj)
