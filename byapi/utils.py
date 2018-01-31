# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

import sys


if sys.version_info[0] == 2:
    PY2 = True
    Byte, Unicode = str, unicode
else:
    PY2 = False
    Byte, Unicode = bytes, str


is_string = lambda s: True if isinstance(s, (Byte, Unicode)) else False
to_unicode = lambda s, e="utf-8": s if isinstance(s, Unicode) else s.decode(e)
to_bytes = lambda s, e="utf-8": s if isinstance(s, Byte) else s.encode(e)
to_str = to_bytes if PY2 else to_unicode


def datetime2str(dt):
    if not dt:
        return ""
    if is_string(dt):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M:%S")
