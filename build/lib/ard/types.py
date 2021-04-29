
class UInteger(int):
    '''
    An int that will be marked as unsigned where necessary.
    '''

class Map:
    '''
    A dict-like object that supports unhashable keys.

    Not optimized for performance.
    '''

    def __init__(self, entries=None):
        self.entries = []
        if isinstance(entries, list) or isinstance(entries, tuple):
            for key, value in entries:
                self.__setitem__(key, value)
        elif isinstance(entries, dict):
            for key, value in entries.items():
                self.__setitem__(key, value)
        elif isinstance(entries, Map):
            for key, value in entries.entries:
                self.__setitem__(key, value)

    def dict(self, strict=False):
        '''
        If cannot be converted to a dict (due to an unhashable key) will
        return self if strict is False, otherwise will raise a TypeError
        '''
        dict_ = {}
        for key, value in self.entries:
            try:
                dict_[key] = value
            except TypeError:
                if strict:
                    raise
                else:
                    return self
        return dict_

    # Mimic the "dict" contract

    def keys(self):
        # TODO: https://docs.python.org/3/library/stdtypes.html#dict-views
        for key, _ in self.entries:
            yield key

    def values(self):
        # TODO: https://docs.python.org/3/library/stdtypes.html#dict-views
        for _, value in self.entries:
            yield value

    def items(self):
        # TODO: https://docs.python.org/3/library/stdtypes.html#dict-views
        return iter(self.entries)

    def clear(self):
        self.entries = []

    def copy(self):
        return Map(self.entries)

    def get(self, key, default=None):
        for key_, value in self.entries:
            if key_ == key:
                return value
        return default

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        for key_, value in self.entries:
            if key_ == key:
                return value
        raise KeyError()

    def __setitem__(self, key, value):
        self.__delitem__(key)
        self.entries.append((key, value))

    def __delitem__(self, key):
        for index, (key_, _) in enumerate(self.entries):
            if key_ == key:
                del self.entries[index]
                return

    def __iter__(self):
        for key, _ in self.entries:
            yield key

    def __eq__(self, other):
        if not isinstance(other, Map):
            return False
        for key, value in self.entries:
            try:
                value_ = other.__getitem__(key)
            except KeyError:
                return False
            if value != value_:
                return False
        for key, value in other.entries:
            try:
                self.__getitem__(key)
            except KeyError:
                return False
        return True

    def __str__(self):
        return str(self.entries)

    def __repr__(self):
        return repr(self.entries)
