
__all__ = (
  'ARDException',
  'EncodeError',
  'DecodeError')


class ARDException(Exception):
  pass


class EncodeError(ARDException):
  pass


class DecodeError(ARDException):
  pass
