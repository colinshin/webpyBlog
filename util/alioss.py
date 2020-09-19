#!/usr/bin/env python
# coding=utf-8

from settings import config
from oss.oss_api import *
from oss import oss_xml_handler
import traceback


class Alicloudoss(object):
    def __init__(self):
        self.oss = OssAPI(config.ALI_OSS_ENDPOINT,
                          config.ALI_OSS_ACCESS_ID,
                          config.ALI_OSS_SECRET_ACCESS_KEY)

    def create_bucket(self, new_bucket):
        res = oss.put_bucket(new_bucket)
        if 2 == (res.status / 100):
            self.err_code(res)
            return True
        else:
            self.err_code(res)
            return False

    def err_code(self, res):
        err_msg = oss_xml_handler.ErrorXml(res.read())

    def buckets(self):
        res = self.oss.list_all_my_buckets()
        if 2 == (res.status / 100):
            http_body = res.read()
            bucket_list = oss_xml_handler.GetServiceXml(http_body)
            return bucket_list.list()
        else:
            return False

    def objects(self, bucket_name):
        res = self.oss.list_bucket(bucket_name)
        if 2 == (res.status / 100):
            data = res.read()
            h = oss_xml_handler.GetBucketXml(data)
            (file_list, common_list) = h.list()
            return file_list
        else:
            return False

    def uploadobj(self, filepath, filename):
        raise Exception("No implementation for uploadobj method")

    def downloadobj(self, filepath, filename):
        res = self.oss.put_object_from_file(self.bucket, filepath, filename,
                                            self.filetype)
        if 2 == (res.status / 100):
            self.err_code(res)
            return True
        else:
            self.err_code(res)
            return False

    def deleteobj(self, bucket, filename):
        res = self.oss.object_operation("DELETE", bucket, filename)
        if 2 == (res.status / 100):
            return True
        else:
            return False


class ImageObj(Alicloudoss):
    def __init__(self):
        Alicloudoss.__init__(self)
        self.filetype = 'image/jpg'
        self.bucket = config.ALI_IMAGE_BUCKET

    def uploadobj(self, filename, filepath):
        filename = "{filedir}/{filename}".format(filedir=config.ALI_OSS_DIR,
                                                 filename=filename)
        res = self.oss.put_object_from_file(self.bucket, filename, filepath,
                                            self.filetype)
        if 2 == (res.status / 100):
            return True
        else:
            return False


class Audioobj(Alicloudoss):
    def __init__(self):
        Alicloudoss.__init__(self)
        self.filetype = 'image/jpg'
        self.bucket = config.ALI_OSS_KEYWORDS

    def uploadobj(self, filepath, filename):
        filename = "{filedir}/{filename}".format(filedir=config.ALI_OSS_DIR,
                                                 filename=filename)
        res = self.oss.put_object_from_file(self.bucket, filename, filepath,
                                            self.filetype)
        if 2 == (res.status / 100):
            return True
        else:
            return False


if __name__ == '__main__':
    try:
        ossiamge = ImageObj()
        ossiamge.uploadobj("test.jpeg",
                           "/opt/apps/webpycms-admin/static/images/"
                           "unknown.jpeg")
    except Exception as e:
        traceback.print_exc()
