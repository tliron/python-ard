
class UInteger(int):
    '''
    An int that will be marked as unsigned where necessary.
    '''

class Map:
    '''
    A dict-like object that supports unhashable keys.

    Not optimized for performance.
    '''

    def __init__(self, entries=None, **kwargs):
        self.entries = []
        self.update(entries, **kwargs)

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
    # See: https://docs.python.org/3/library/stdtypes.html#dict

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

    def get(self, key, default=None):
        for key_, value in self.entries:
            if key_ == key:
                return value
        return default

    def pop(self, key, **kwargs):
        for index, (key_, value) in enumerate(self.entries):
            if key_ == key:
                del self.entries[index]
                return value
        try:
            return kwargs['default']
        except KeyError:
            raise KeyError(key)

    def popitem(self):
        return self.entries.pop()

    def setdefault(self, key, default=None):
        for key_, value in self.entries:
            if key_ == key:
                return value
        self.entries.append((key, value))
        return default

    def update(self, other=None, **kwargs):
        if other is not None:
            try:
                # List of tuples
                for key, value in other:
                    self.__setitem__(key, value)
            except TypeError:
                # Dict-like object
                for key in other:
                    self.__setitem__(key, other[key])

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def clear(self):
        self.entries = []

    def copy(self):
        copy = Map()
        copy.entries = list(self.entries)
        return copy

    # See: https://docs.python.org/3/reference/datamodel.html

    def __len__(self):
        return len(self.entries)

    def __contains__(self, key):
        for key_, value in self.entries:
            if key_ == key:
                return True
        return False

    def __getitem__(self, key):
        for key_, value in self.entries:
            if key_ == key:
                return value
        raise KeyError(key)

    def __setitem__(self, key, value):
        for index, entry in enumerate(self.entries):
            if entry[0] == key:
                entry[1] = value
                return
        self.entries.append((key, value))

    def __delitem__(self, key):
        for index, (key_, _) in enumerate(self.entries):
            if key_ == key:
                del self.entries[index]
                return

    def __iter__(self):
        for key, _ in self.entries:
            yield key

    def __or__(self, other): # self | other
        copy = self.copy()
        copy.update(other)
        return copy

    def __ror__(self, other): # other | self
        other = Map(other)
        other.update(self)
        return other

    def __ior__(self, other): # self |= other
        self.update(other)
        return self

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
