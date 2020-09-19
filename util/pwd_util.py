# -*- coding:utf-8 -*-

import hashlib
import os
import random
import time
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random

from settings import config


def make_sms_code():
    """
    短信验证码
    :return:
    """
    return str(random.randint(1000, 9999))


def create_md5(args):
    md5_constructor = hashlib.md5
    return md5_constructor(args.encode("utf8")).hexdigest()


def admin_pwd_digest(passwd):
    """
    用户加密密码处理
    :param passwd:
    :return:
    """
    ttt = config.ADMIN_SECRET + passwd
    return create_md5(ttt)


class AESManager(object):
    def __init__(self, key=config.ASE_KEY):
        self.bs = 32
        if len(key) >= 32:
            self.key = key[:32]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.urlsafe_b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.urlsafe_b64decode(enc.strip())
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_without_hot_key(self, enc):
        """
        加密不带key
        :param hot_key:
        :param enc:
        :return:
        """
        enc = "==x*||".join(map(str, enc))
        enc = base64.urlsafe_b64decode(enc.strip())
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(
            self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


if __name__ == "__main__":
    # data = [51, 1, 29, 6]
    # aes = AESManager()
    # print aes.encrypt("==x*||".join(map(str, data)))
    # key = "l6w0PqTu2t08HImvTsUvAl220wRHrpzUbYSU_FGnBgdxa8EL5WKwldYNZHyeNsuq"
    # print aes.decrypt(key).split("=1=")
    print(admin_pwd_digest('admin123'))
