# -*- coding: utf-8 -*-

import time
from util.log import log
import uuid
import hashlib

timetoolong = []


def uuidgen():
    return str(uuid.uuid4())


def hashgen(s):
    return hashlib.sha224(s).hexdigest()


def counttime(func):
    def _warpper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        spent_time = time.time() - start_time
        log.info("%s time spent is %f" % (func.__name__, spent_time))
        if spent_time > 0.01:
            timetoolong.append([spent_time])
        return result

    return _warpper
