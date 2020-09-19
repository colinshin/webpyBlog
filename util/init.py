# coding=utf-8


from models.albums import Albums
from models.article_comments import ArticleComments

from models.articles import Articles
from models.base import db
from models.categories import Categories
from models.images import Images
from models.users import Users
from models.version import Version


class DbInit(object):
    def __init__(self):
        db.connect()

        tables = [
            Albums,
            ArticleComments,
            Articles,
            Categories,
            Images,
            Users,
            Version,
        ]

        if not Version.table_exists():
            db.create_tables(tables)

        self.version, _ = Version.get_or_create(description="0.1")
        self.default_thumbnail = "data:image/jpg;base64,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"
        # self.default_thumbnail = base64.b64encode(
        #     buffer(Imaging.default_thumbnail()))

        self.sys_categories, _ = Categories.get_or_create(
            name='系统分类',
            description='初始父类!',
            thumbnail=self.default_thumbnail,
        )
        self.article_categories = Categories.create(
            name='文章',
            description='文章',
            thumbnail=self.default_thumbnail,
            parent=self.sys_categories
        )

        self.admin, _ = Users.get_or_create(
            name='admin',
            cellphone='19999999999',
            email='admin@webpy.cn',
            address='陕西西安',
            birthday='2020.9',
            password='3981c2d8a3917de70be4ff59e2f68b30',
            gender=0,
            description='系统管理员!',
            avatar=self.default_thumbnail
        )

        self.sys_album, _ = Albums.get_or_create(
            name='系统专辑',
            description='系统专辑!',
            thumbnail=self.default_thumbnail,
            owner=self.admin
        )

        self.sys_image, _ = Images.get_or_create(
            description='系统图片!',
            thumbnail=self.default_thumbnail,
            owner=self.admin,
            album=self.sys_album,
            uuid='default'
        )

    def print_trace_log(self):
        print('Database Version: %s' % self.version.description)
        print('Administrator: name=%s, cellphone=%s, email=%s' % (self.admin.name,
                                                                self.admin.cellphone,
                                                                self.admin.email))
        print('Predefined System Album: name=%s, desc=%s' % (
        self.sys_album.name, self.sys_album.description))
        print('Predefined System Image: uuid=%s, desc=%s' % (
        self.sys_image.uuid, self.sys_image.description))


def init():
    db_init = DbInit()
    db_init.print_trace_log()


if __name__ == '__main__':
    db_init = DbInit()
    db_init.print_trace_log()
