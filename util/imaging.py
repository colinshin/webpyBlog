# -*- coding: utf-8 -*-
# coding=utf-8

import os
from io import StringIO
from settings import config
from PIL import Image


class Imaging(object):
    def __init__(self, file_obj):
        self.file_obj = file_obj
        file_obj.seek(0)
        self.im = Image.open(self.file_obj)

    def format(self):
        return self.im.format.lower()

    def size(self):
        return self.im.size

    def resize(self, xres, yres, quality=config.IMAGE_QUALITY,
               dpi=config.IMAGE_DPI, format='JPEG'):
        img = self.im
        # To workaround issue against cannot write mode P as JPEG      
        if img.mode != 'RGB':
            img = img.convert('RGB')

        resized = img.resize((xres, yres), Image.ANTIALIAS)
        output = StringIO()
        resized.save(output, format, dpi=dpi, quality=quality)
        return output.getvalue()

    def thumbnail(self,
                  xres=config.THUMBNAIL_XRES,
                  yres=config.THUMBNAIL_YRES,
                  quality=config.IMAGE_QUALITY,
                  dpi=config.IMAGE_DPI, format='JPEG'):
        img = self.im
        # To workaround issue against cannot write mode P as JPEG      
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.thumbnail((xres, yres), Image.ANTIALIAS)
        output = StringIO()
        img.save(output, format, dpi=dpi, quality=quality)
        return output.getvalue()

    @staticmethod
    def default_thumbnail():
        file_object = open('static/images/default.jpeg', 'r')
        im = Imaging(file_object)

        return im.resize(int(im.size()[0] / config.THUMBNAIL_XRES),
                         int(im.size()[1] / config.THUMBNAIL_YRES),
                         config.THUMBNAIL_QUALITY,
                         config.THUMBNAIL_DPI)

    @staticmethod
    def system_thumbnail(key):
        file_object = open('static/images/default.jpeg', 'r')
        im = Imaging(file_object)

        return im.resize(int(im.size()[0] / config.THUMBNAIL_XRES),
                         int(im.size()[1] / config.THUMBNAIL_YRES),
                         config.THUMBNAIL_QUALITY,
                         config.THUMBNAIL_DPI)


if __name__ == '__main__':
    example = '..\\static\\images\\logo.png'
    buf = open(os.path.join(config.ROOT_DIR, example), 'rb').read()
    im = Imaging(StringIO(buf))
    print(im.size())
    open('/tmp/out.jpeg', 'w').write(im.resize(80, 60))
