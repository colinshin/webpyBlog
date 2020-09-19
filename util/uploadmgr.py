# -*- coding: utf-8 -*-

import os
from settings import config
from .utils import uuidgen
import magic
import traceback
from .log import log


class HttpUploadedFile(object):
    def __init__(self, raw_data):
        self._mimetype = None
        self._uuid = uuidgen()

        try:
            self._mimetype = \
                magic.from_buffer(raw_data, mime=True).lower().split(';')[0]
            log.info(self._mimetype)
        except Exception:
            log.error(traceback.format_exc())
            self._mimetype = None

        if self._mimetype not in ['application/zip', 'application/octet-stream',
                                  'audio/mpeg', 'image/jpeg', 'image/bmp',
                                  'image/png', 'image/gif', 'image/webp',
                                  'video/mp4']:
            raise Exception('mimetype not supported!')

        # workaround against mp3 suffix
        if self._mimetype == 'audio/mpeg':
            self._mimetype = 'audio/mp3'

        self._filename = '%s.%s' % (self._uuid, 'jpeg')

    def uuid(self):
        return self._uuid

    def filename(self):
        return self._filename

    def mimetype(self):
        return self._mimetype


class HttpFileSystem(object):
    def __init__(self):
        self.upload_dir = config.UPLOAD_DIR
        self.image_dir = os.path.join(self.upload_dir, 'image')

    def image_url_from_uuid(self, uuid):
        return os.path.join(self.image_dir, '%s.jpeg' % uuid)
