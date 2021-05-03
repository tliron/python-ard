
import collections.abc

__all__ = (
    'UInteger',
    'Map')


class UInteger(int):
    '''
    An int that will be marked as unsigned where necessary.
    '''


class Map(collections.abc.MutableMapping):
    '''
    A dict-like object that supports arbitrary, even unhashable keys.
    The cost is worst-case performance: implemented as a list rather than a hashtable.
    Iteration retains insertion order.
    Not thread-safe.
    '''

    def __init__(self, entries=None, **kwargs):
        self.entries = []
        self.update(entries, **kwargs)

    def dict(self, strict=False):
        '''
        Attempt to convert to a dict.
        If cannot be converted (due to an unhashable key) will return self
        if strict is False, otherwise will raise a TypeError
        '''
        dict_ = {}
        for key, value in self.entries:
            try:
                dict_[key] = value
            except TypeError:
                # Unhashable key, so cannot be converted to a dict
                if strict:
                    raise
                else:
                    return self
        return dict_

    # JSON serializable

    # Mimic the "dict" contract
    # See: https://docs.python.org/3/library/stdtypes.html#dict

    def keys(self):
        return _MapKeys(self)

    def values(self):
        return _MapValues(self)

    def items(self):
        return _MapItems(self)

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
        self.entries.append((key, default))
        return default

    def update(self, other=None, **kwargs):
        if other is not None:
            try:
                # List of tuples
                for key, value in other:
                    self.__setitem__(key, value)
            except ValueError:
                # Dict-like object
                for key in other:
                    self.__setitem__(key, other[key])

        for key, value in kwargs.items():
            self.__setitem__(key, value)
        
        return None

    def clear(self):
        self.entries = []

    def copy(self):
        copy = Map()
        copy.entries = list(self.entries)
        return copy

    # See: https://docs.python.org/3/reference/datamodel.html

    def __hash__(self):
        return hash(tuple(self.entries))

    def __len__(self):
        return len(self.entries)

    def __contains__(self, key):
        for key_, _ in self.entries:
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

    def __reversed__(self):
        for key, _ in reversed(self.entries):
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
        '''
        Equality does not take insertion order into consideration.
        '''
        if not isinstance(other, collections.abc.Mapping):
            return False
        if len(self.entries) != len(other):
            return False
        for key, value in self.entries:
            try:
                if value != other[key]:
                    return False
            except (KeyError, TypeError):
                return False
        return True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{' + ', '.join((repr(k) + ': ' + repr(v) for k, v in self.entries)) + '}'

collections.abc.MutableMapping.register(Map)

# Views
# See: https://docs.python.org/3/library/stdtypes.html#dict-views

class _MapKeys(collections.abc.KeysView):
    def __contains__(self, key):
        for key_, _ in self._mapping.entries:
            if key_ == key:
                return True
        return False

    def __iter__(self):
        for key, _ in self._mapping.entries:
            yield key

    def __reversed__(self):
        for key, _ in reversed(self._mapping.entries):
            yield key

collections.abc.KeysView.register(_MapKeys)

class _MapValues(collections.abc.ValuesView):
    def __contains__(self, value):
        for _, value_ in self._mapping.entries:
            if value_ == value:
                return True
        return False

    def __iter__(self):
        for _, value in self._mapping.entries:
            yield value

    def __reversed__(self):
        for _, value in reversed(self._mapping.entries):
            yield value

collections.abc.ValuesView.register(_MapValues)

class _MapItems(collections.abc.ItemsView):
    def __contains__(self, entry):
        return entry in self._mapping.entries

    def __iter__(self):
        yield from self._mapping.entries

    def __reversed__(self):
        yield from reversed(self._mapping.entries)

collections.abc.ItemsView.register(_MapItems)
