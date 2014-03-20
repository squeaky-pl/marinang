from cffi import FFI
from subprocess import check_output
import os
import distutils.log
import shlex


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
void mysql_close(MYSQL *sock);
""")

cflags = shlex.split(check_output(['mysql_config', '--cflags']))
libraries = shlex.split(check_output(['mysql_config', '--libs']))


distutils.log.set_verbosity(1 if 'MARINA_VERBOSE' in os.environ else 0)

lib = ffi.verify("""

#include <mysql/mysql.h>

""", extra_compile_args=cflags, extra_link_args=libraries)


globals().update(lib.__dict__)
globals()['string'] = ffi.string
globals()['NULL'] = ffi.NULL
