Agnostic Raw Data for Python
============================

See the description of Agnostic Raw Data (ARD) in the
[Go ARD library](https://github.com/tliron/kutil/tree/main/ard).

The latest stable release of this library is
[available on PyPi](https://pypi.org/project/ard/):

    python -m pip install ard

This library has three main features:

1. Allows you to easily transmit ARD in several formats: YAML, JSON, XML, and
   CBOR. Supports both encoding and decoding. Included is an `ardconv` CLI
   tool that can convert between all formats.
2. Enable support for decoding YAML with complex keys. As it stands, the
   otherwise excellent [ruamel.yaml](https://pypi.org/project/ruamel.yaml/)
   library will choke on complex keys.
3. Support for ARD-compatible extensions to JSON (CJSON). This allows for
   round-tripping ARD through JSON without losing type information, including
   support for integers, byte arrays, and maps with non-string keys.

Python's `dict` does not support un-hashable keys, making it difficult to work
with complex keys. For this reason we provide the `ard.Map` class, which does
support un-hashable keys and is otherwise a drop-in replacement for `dict`. It
will be used automatically when decoding, if necessary.

Documentation is a work in progress! For now check out [`test.py`](test.py)
for example use.
