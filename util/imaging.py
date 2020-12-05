# -*- coding: utf-8 -*-
# coding=utf-8
import base64
import hashlib
import os
from io import BytesIO
from settings import config
from PIL import Image, ImageDraw, ImageFont


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
        output = BytesIO()
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
        output = BytesIO()
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


class GenImage(object):
    def __init__(self):
        self.ins = Image.new('RGBA', (480, 300), color="rgb(108,158,210)")
        self.draw = ImageDraw.Draw(self.ins)  # 480x300

    @staticmethod
    def is_chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def get_char_length(self, char):
        str_len = 0
        for s in char:
            if self.is_chinese(s):
                str_len += 2
            else:
                str_len += 1
        str_length_half = str_len * 45 / 2
        start_x = 240 - str_length_half
        return start_x

    def save(self, char):
        self.draw.text((self.get_char_length(char), 95),
                       text=char,
                       font=ImageFont.truetype('simhei.ttf', 90),
                       fill='#ffffff',
                       align="center")
        m = hashlib.md5()
        m.update(char.encode("utf-8"))
        m.hexdigest()
        file_name = m.hexdigest() + ".jpg"
        file_path = os.path.realpath(os.path.join(config.STATIC_DIR, "images", file_name))
        try:
            self.ins.save(file_path)
            return True, file_name
        except Exception as e:
            print(e)
            return False, ""

    def save2base64(self, char):
        self.draw.text((self.get_char_length(char), 95),
                       text=char,
                       font=ImageFont.truetype('simhei.ttf', 90),
                       fill='#ffffff',
                       align="center")
        output_buffer = BytesIO()
        self.ins.save(output_buffer, format='png')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return b'data:image/png;base64,' + base64_str


# if __name__ == '__main__':
#     size = 14
#     font = ImageFont.truetype('simhei.ttf', size)
#     hans = ["python", "html", "javascript", "nginx", "数据库"]
#     for han in hans:
#         image = gen_font_image(han)
#         image.save(str(hans.index(han)) + '.png')
#
# if __name__ == '__main__':
#     example = '..\\static\\images\\logo.png'
#     buf = open(os.path.join(config.ROOT_DIR, example), 'rb').read()
#     im = Imaging(StringIO(buf))
#     print(im.size())
#     open('/tmp/out.jpeg', 'w').write(im.resize(80, 60))
