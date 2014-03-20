from marinang import client
from marinang.compat import string_types


def test_version():
    assert isinstance(client.version, string_types)


def test_decversion():
    assert isinstance(client.decversion, int)


def test_version_info():
    info = client.version_info

    assert len(info) == 3
    assert (info[0], info[1], info[2]) == (info.major, info.minor, info.micro)
