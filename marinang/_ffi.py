from cffi import FFI
from subprocess import check_output
import os
import distutils.log
import shlex
import functools


ffi = FFI()

ffi.cdef("""

typedef ... MYSQL;

MYSQL * mysql_init(MYSQL *mysql);

const char * mysql_get_client_info(void);
unsigned long mysql_get_client_version(void);
const char * mysql_error(MYSQL *mysql);
MYSQL * mysql_real_connect(
    MYSQL *mysql, const char *host, const char *user, const char *passwd,
    const char *db, unsigned int port, const char *unix_socket,
    unsigned long clientflag);
int mysql_query(MYSQL *mysql, const char *q);
void mysql_close(MYSQL *sock);
""")

can_err = [
    'init',
    'real_connect',
    'query',
]

can_pass_none = [
    'init',
    'real_connect'
]

cflags = shlex.split(check_output(['mysql_config', '--cflags']))
libraries = shlex.split(check_output(['mysql_config', '--libs']))


distutils.log.set_verbosity(1 if 'MARINA_VERBOSE' in os.environ else 0)

lib = ffi.verify("""

#include <mysql/mysql.h>

""", extra_compile_args=cflags, extra_link_args=libraries)


class ServerException(Exception):
    pass


def check_for_error(func):
    kind = ffi.typeof(func).result.kind

    def wrapper(*args):
        result = func(*args)

        if kind == 'pointer' and result == ffi.NULL or \
           kind == 'primitive' and result != 0:
                raise ServerException(ffi.string(lib.mysql_error(args[0])))

        return result

    return wrapper


def escape_none(func):
    @functools.wraps(func)
    def wrapper(*args):
        return func(*[ffi.NULL if a is None else a for a in args])

    return wrapper


for name, func in lib.__dict__.items():
    if not name.startswith('mysql_'):
        continue

    name = name[6:]

    if name in can_err:
        func = check_for_error(func)

    if name in can_pass_none:
        func = escape_none(func)

    globals()[name] = func


string = ffi.string
NULL = ffi.NULL
