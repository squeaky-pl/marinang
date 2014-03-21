import types
import sys
from collections import namedtuple

from marinang import _ffi


VersionInfo = namedtuple('VersionInfo', 'major minor micro')


class ClientModule(types.ModuleType):
    def __init__(self, _ffi, VersionInfo):
        self.VersionInfo = VersionInfo
        self._ffi = _ffi
        types.ModuleType.__init__(self, __name__)

    @property
    def version(self):
        return self._ffi.string(self._ffi.get_client_info())

    @property
    def decversion(self):
        return int(self._ffi.get_client_version())

    @property
    def version_info(self):
        rest, micro = divmod(self.decversion, 100)
        major, minor = divmod(rest, 100)

        return self.VersionInfo(major, minor, micro)


sys.modules[__name__] = ClientModule(_ffi, VersionInfo)
