## webpyCMS

webpyCMS是基于web.py的网站内容管理系统，小巧实用，非常适合做博客和个人简历网站。

当前版本为0.2，搭好了基本框架，简单实现了分类、文章的后台管理，前端（使用了bootstrap框架）展示。

项目基于 python3+peewee+templator完成。

## 功能

- 后台文章，分类，相册，图片的新增，编辑功能
- 后台配置网站信息（设置网站个人信息，网站备案号和版权信息）
- 实现文章的搜索功能
- 文章的标签及列表功能
- 文章的分类和列表功能  
- 根据设置的相册显示配置的图片和链接
- 添加友情链接功能
- 初步实现个人简历页面


## 使用步骤

1、下载代码

2、安装依赖 pip install -r requirements.txt

3、创建数据库 webpycms, 执行 webpycms.sql 初始化数据表结构和初始数据

4、设置配置信息（开发模式及产品模式下的web_url参数，这里会影响首页的轮播图现实）

5、执行 python manage.py 运行程序

6、访问 http://127.0.0.1:8080

7 管理后台访问地址 http://127.0.0.1:8080/admin/login， 账号admin 密码admin123

8、截图

![Image text](https://raw.githubusercontent.com/colinshin/webpyCMS/master/static/images/one.png)

![Image text](https://raw.githubusercontent.com/colinshin/webpyCMS/master/static/images/two.png)

