# coding=utf-8

import os


class DevelopConfig(object):
    # Debugging
    DEBUG = 0

    # Site information
    NAME = 'webpyCMS'
    DESCRIPTION = 'webpyCMS'
    CSS = 'static/'
    TEMPLATE = 'templates/'
    FRONT_TEMPLATE = 'templates/front/'
    ADMIN_TEMPLATE = 'templates/admin/'
    ADMIN_SECRET = 'styt@3dfgs'
    ASE_KEY = '$sdfas'
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__)).split('settings')[0]

    # Accounts
    ADMIN_USERNAME = 'cmsadmin'
    ADMIN_PASSWORD = 'admin@9000'

    # Count
    PAGINATE_COUNT = 25

    # Paths
    ROOT_DIR = os.getcwd()
    DATA_DIR = os.path.join(ROOT_DIR, 'data')
    TMPL_DIR = os.path.join(ROOT_DIR, TEMPLATE)
    FRONT_TMPL_DIR = os.path.join(ROOT_DIR, FRONT_TEMPLATE)
    ADMIN_TMPL_DIR = os.path.join(ROOT_DIR, ADMIN_TEMPLATE)
    VIEW_DIR = os.path.join(ROOT_DIR, 'views')
    STATIC_DIR = os.path.join(ROOT_DIR, 'static')
    STATIC_CSS_DIR = os.path.join(ROOT_DIR, CSS)
    UPLOAD_DIR = os.path.join(STATIC_DIR, 'uploads')

    # URLs
    WEB_URL = 'http://127.0.0.1:8080/'
    ADMIN_URL = 'http://admin.webpycms.com'
    API_URL = 'http://api.webpycms.com'
    ALI_CDNIMAGES_URL = 'http://images.webpycms.com' if not os.getenv(
        'ALI_OSS_KEYWORDS') else "http://%s-images.%s.com" % (
        os.getenv('ALI_OSS_KEYWORDS'), os.getenv('ALI_OSS_KEYWORDS'))
    ALI_CDNSTATIC_URL = 'http://images.webpycms.com' if not os.getenv(
        'ALI_OSS_KEYWORDS') else "http://%s-static.%s.com" % (
        os.getenv('ALI_OSS_KEYWORDS'), os.getenv('ALI_OSS_KEYWORDS'))
    CDNSTATIC_URL = 'http://images.webpycms.com'
    STATIC_LOCAL_URL = 'http://127.0.0.1:8080'

    # Configuration Maximum
    MAX_UPLOAD_FILE_SIZE = 4 * 1024 * 1024

    # Database
    DB_NAME = 'webpycms'
    DB_USER = 'root'
    DB_PASSWORD = '123456'
    DB_HOST = '127.0.0.1'

    # Options
    LOC_TRANSMIT = True

    # Imaging
    THUMBNAIL_XRES = 3
    THUMBNAIL_YRES = 3
    THUMBNAIL_QUALITY = 90
    THUMBNAIL_DPI = (120, 120)

    IMAGE_XRES = 1
    IMAGE_YRES = 1
    IMAGE_QUALITY = 80
    IMAGE_DPI = (100, 100)

