from helpers import *

def test_num2str():
    assert num2str(1) == '\x01'
    assert num2str(256) == '\x01\x00'
    assert num2str(65536) == '\x01\x00\x00'
    assert num2str(6382179) == 'abc'
    assert num2str(113685359126373) == 'george'


def test_str2num():
    assert str2num('\x01') == 1
    assert str2num('\x01\x00') == 256
    assert str2num('\x01\x00\x00') == 65536
    assert str2num('abc') == 97*256**2 + 98*256 + 99
    assert str2num('george') == 113685359126373
