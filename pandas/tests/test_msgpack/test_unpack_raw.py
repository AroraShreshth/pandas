"""Tests for cases where the user seeks to obtain packed msgpack objects"""

import six
from pandas.msgpack import Unpacker, packb


def test_write_bytes():
    unpacker = Unpacker()
    unpacker.feed(b'abc')
    f = six.BytesIO()
    assert unpacker.unpack(f.write) == ord('a')
    assert f.getvalue() == b'a'
    f = six.BytesIO()
    assert unpacker.skip(f.write) is None
    assert f.getvalue() == b'b'
    f = six.BytesIO()
    assert unpacker.skip() is None
    assert f.getvalue() == b''


def test_write_bytes_multi_buffer():
    long_val = (5) * 100
    expected = packb(long_val)
    unpacker = Unpacker(six.BytesIO(expected), read_size=3, max_buffer_size=3)

    f = six.BytesIO()
    unpacked = unpacker.unpack(f.write)
    assert unpacked == long_val
    assert f.getvalue() == expected
