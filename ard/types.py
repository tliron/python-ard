
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

    Note: Getting the hash of an instance will cause it to become immutable
    because we cannot allow the hash to change from that point onward.
    '''

    def __init__(self, items=None, **kwargs):
        self._items = []
        self._mutable = True
        self._hash = None
        self.update(items, **kwargs)

    def freeze(self):
        self._mutable = False

    def dict(self, strict=False, json=False):
        '''
        Attempt to convert to a dict.
        If cannot be converted (due to an incompatible key) will return self if strict is False,
        otherwise will raise a TypeError.
        '''
        dict_ = {}
        for key, value in self._items:
            try:
                if json and not isinstance(key, (str, int, float, bool, None)):
                    # JSON has strict requirements for key types beyond them being hashable
                    raise TypeError()
                dict_[key] = value
            except TypeError:
                # Cannot be converted to a dict
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
        for key_, value in self._items:
            if key_ == key:
                return value
        return default

    def pop(self, key, **kwargs):
        if not self._mutable:
            raise TypeError('this Map is immutable')
        for index, (key_, value) in enumerate(self._items):
            if key_ == key:
                del self._items[index]
                return value
        try:
            return kwargs['default']
        except KeyError:
            raise KeyError(key)

    def popitem(self):
        if not self._mutable:
            raise TypeError('this Map is immutable')
        return self._items.pop()

    def setdefault(self, key, default=None):
        if not self._mutable:
            raise TypeError('this Map is immutable')
        for key_, value in self._items:
            if key_ == key:
                return value
        self._items.append((key, default))
        return default

    def update(self, other=None, **kwargs):
        if not self._mutable:
            raise TypeError('this Map is immutable')
        if other is not None:
            if isinstance(other, collections.abc.Mapping):
                # Dict-like object
                for key in other:
                    self.__setitem__(key, other[key])
            else:
                # List of tuples
                for key, value in other:
                    self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)
        
        return None

    def clear(self):
        if not self._mutable:
            raise TypeError('this Map is immutable')
        self._items = []

    def copy(self):
        copy = Map()
        copy._items = list(self._items)
        return copy

    # See: https://docs.python.org/3/reference/datamodel.html

    def __hash__(self):
        self.freeze()
        if self._hash is None:
            self._hash = hash(tuple(self._items))
        return self._hash

    def __len__(self):
        return len(self._items)

    def __contains__(self, key):
        for key_, _ in self._items:
            if key_ == key:
                return True
        return False

    def __getitem__(self, key):
        for key_, value in self._items:
            if key_ == key:
                return value
        raise KeyError(key)

    def __setitem__(self, key, value):
        if not self._mutable:
            return NotImplemented
        for index, item in enumerate(self._items):
            if item[0] == key:
                item[1] = value
                return
        self._items.append((key, value))

    def __delitem__(self, key):
        if not self._mutable:
            return NotImplemented
        for index, (key_, _) in enumerate(self._items):
            if key_ == key:
                del self._items[index]
                return

    def __iter__(self):
        for key, _ in self._items:
            yield key

    def __reversed__(self):
        for key, _ in reversed(self._items):
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
        if not self._mutable:
            return NotImplemented
        self.update(other)
        return self

    def __eq__(self, other):
        '''
        Equality does not take insertion order into consideration.
        '''
        if not isinstance(other, collections.abc.Mapping):
            return False
        if len(self._items) != len(other):
            return False
        for key, value in self._items:
            try:
                if value != other[key]:
                    return False
            except (KeyError, TypeError):
                return False
        return True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{' + ', '.join((repr(k) + ': ' + repr(v) for k, v in self._items)) + '}'

collections.abc.MutableMapping.register(Map)

# Views
# See: https://docs.python.org/3/library/stdtypes.html#dict-views

class _MapKeys(collections.abc.KeysView):
    def __contains__(self, key):
        for key_, _ in self._mapping._items:
            if key_ == key:
                return True
        return False

    def __iter__(self):
        for key, _ in self._mapping._items:
            yield key

    def __reversed__(self):
        for key, _ in reversed(self._mapping._items):
            yield key

collections.abc.KeysView.register(_MapKeys)

class _MapValues(collections.abc.ValuesView):
    def __contains__(self, value):
        for _, value_ in self._mapping._items:
            if value_ == value:
                return True
        return False

    def __iter__(self):
        for _, value in self._mapping._items:
            yield value

    def __reversed__(self):
        for _, value in reversed(self._mapping._items):
            yield value

collections.abc.ValuesView.register(_MapValues)

class _MapItems(collections.abc.ItemsView):
    def __contains__(self, item):
        return item in self._mapping._items

    def __iter__(self):
        yield from self._mapping._items

    def __reversed__(self):
        yield from reversed(self._mapping._items)

collections.abc.ItemsView.register(_MapItems)
