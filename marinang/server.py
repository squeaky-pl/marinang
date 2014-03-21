import _ffi


class Connection(object):
    def __init__(self):
        self.__handle = _ffi.init(None)

    @classmethod
    def _connect(klass, host=None, user=None, password=None, database=None,
                 port=None, socket=None, **kwargs):

        port = port or 0
        connection = klass()
        _ffi.real_connect(
            connection.__handle, host, user, password, database, port, socket,
            0)

        return connection

    def query(self, sql):
        _ffi.query(self.__handle, sql)

    def close(self):
        _ffi.close(self.__handle)
        self.__handle = None

    @property
    def closed(self):
        return not self.__handle

    def __del__(self):
        if not self.closed:
            self.close()


connect = Connection._connect
del Connection._connect
