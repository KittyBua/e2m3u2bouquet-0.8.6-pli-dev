# logging
#
# One can simply use
# import log
# print>>log, "Some text"
# because the log unit looks enough like a file!

import sys
import threading
PY3 = sys.version_info.major >= 3

if PY3:
    import io
    from io import StringIO
    logfile = io.StringIO()
else:
    from cStringIO import StringIO
    logfile = StringIO()


# Need to make our operations thread-safe.
mutex = threading.Lock()


def write(data):
    mutex.acquire()
    try:
        if logfile.tell() > 2000:
            # Do a sort of 2k round robin
#            logfile.reset()
            logfile.seek(0)
        logfile.write(data)
    finally:
        mutex.release()
    sys.stdout.write(data)


def getvalue():
    mutex.acquire()
    try:
        pos = logfile.tell()
        head = logfile.read()
#        logfile.reset()
        logfile.seek(0)
        tail = logfile.read(pos)
    finally:
        mutex.release()
    return head + tail
