# -*- coding: utf-8 -*-

import logging
import os
from settings import config


def logger():
    # 创建logger，如果参数为空则返回root logger
    log = logging.getLogger("webpycms")
    log.setLevel(logging.DEBUG)  # 设置logger日志等级
    log_dir = os.path.abspath(os.path.join(config.ROOT_DIR, '/logs/'))
    log_file = os.path.realpath(os.path.normpath(os.path.join(log_dir,
                                                              'webpycms.log')))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(log_file):
        with open(log_file, "a+") as fp:
            pass
        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not log.handlers:
        # 创建handler
        fh = logging.FileHandler(log_file, encoding="utf-8")
        ch = logging.StreamHandler()

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt="%(asctime)s|%(name)s|%(levelname)s|%(filename)s|%(funcName)s|%(lineno)d|%(message)s",
            datefmt="%Y/%m/%d %X"
        )

        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 为logger添加的日志处理器
        log.addHandler(fh)
        log.addHandler(ch)

    return log  # 直接返回logger


log = logger()

if __name__ == "__main__":
    import time
    while True:
        time.sleep(0.5)
        log.warning("泰拳警告")
        log.info("提示")
        log.error("错误")
        log.debug("查错")
