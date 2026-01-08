# [项目名称]-后端

本项目后端基于 Matrix 工作室 Django 项目模板创建，提前内置了 DRF 等第三方开发库，可以极大的提高开发效率，避免重复造轮子。

跟标准的 Django 项目的区别还有：
1. settings 配置文件转移到了 Backend/Backend/settings 文件夹内，base.py 中是基础配置，dev.py 代表的是开发环境配置，test.py 代表的是测试环境配置，prod.py 代表的是生产环境配置；
2. startapp 创建的应用转移到了 Backend/Backend/apps 文件夹内，每一个文件夹代表了一个应用，如果要新建应用的话，需要先 `cd Backend/apps`然后在再`python ../../manage.py startapp ApplicationName`（注意应用首字母要大写）；

## 快速开始

1. 项目代码拉取下来后，首先需要迁移数据库

```shell
python manage.py makemigrations
python manage.py migrate
```

2. 创建超级管理员账户

```shell
python manage.py createsuperuser
```

开发环境和测试环境，用户名和密码在都是 admin。

3. 在本地（一般是自己的电脑）开发的话，通过 `python manage.py runserver`启动，默认加载的是 `Backend/Backend/settings/dev.py`，即在本地创建一个 db.sqlite3 数据库，所有的数据都在本地；

