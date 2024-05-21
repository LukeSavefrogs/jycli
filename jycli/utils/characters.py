""" Utilities for handling characters in Python 2 and 3. 

Python 3 has default support for Unicode characters, while Python 2 requires explicit conversion.
"""
import re as _re
import sys as _sys

REGEX_ASCII = _re.compile(r'[^\x00-\x7F]')

# On Jython 2.1, the `len()` function over a unicode string returns a wrong value:
# wsadmin>len("│") # expect: 1
# 3
# 
# This is solved by explicitly converting the string from UTF8 to unicode and then getting the length:
# wsadmin>len(unicode("│", "utf-8")) # expect: 1
# 1
#
# Source: https://stackoverflow.com/a/16476580/8965861
if _sys.version_info < (3, 0, 0):
  text_type = unicode
  binary_type = str
  def b(x):
    return x
  def u(x):
    """ Convert a string to unicode (on Py3 this has no effect). """
    return unicode(x, "utf-8")
else:
  text_type = str
  binary_type = bytes
  import codecs
  def b(x):
    return codecs.latin_1_encode(x)[0]
  def u(x):
    """ Convert a string to unicode (on Py3 this has no effect). """
    return x



def is_ascii(text):
    # type: (str) -> bool
    """ Check if a string contains only ASCII characters.

    Args:
        text (str): The string to check.

    Example:
        ```
        >>> is_ascii("Hello, World!")
        True
        >>> is_ascii("你好，世界！")
        False
        ```

    Source:
        https://stackoverflow.com/a/40309367/8965861
    """
    return REGEX_ASCII.search(text) is None
