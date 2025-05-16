# Jens Blog - 个人博客系统

这是一个使用Django框架开发的个人博客系统，具有用户注册、登录、发布文章、编辑文章等功能。

## 功能特点

- 用户注册和登录系统
- 发布博客文章
- 查看所有文章列表
- 查看单篇文章详情
- 更新已发布的文章
- 删除文章
- 文章分类和标签功能
- 文章评论和回复系统
- 全站搜索功能（支持标题和内容搜索）
- 搜索结果关键词高亮显示
- 用户个人中心
- 邮箱验证码注册功能
- 防CSRF和XSS攻击安全措施
- 社交媒体分享功能（微信、微博、QQ等）
- 使用MySQL数据库

## 环境要求

- Python 3.8+
- Django 4.2+
- MySQL 5.7+

## 安装步骤

1. 克隆项目到本地
2. 创建虚拟环境（可选）
3. 安装依赖

```bash
pip install django pymysql
```

4. 配置数据库（MySQL）

在MySQL中执行以下命令创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS jens_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. 修改数据库连接信息

编辑`jens_blog/settings.py`文件中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jens_blog',
        'USER': '你的MySQL用户名',
        'PASSWORD': '你的MySQL密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

7. 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

8. 启动开发服务器

```bash
python manage.py runserver
```

## 使用方法

1. 访问 http://127.0.0.1:8000/ 进入博客首页
2. 注册新用户或使用已有账号登录
3. 登录后可以创建、编辑和删除自己的文章
4. 使用页面侧边栏的搜索框可以搜索全站文章
5. 通过标签和分类可以筛选相关文章
6. 访问 http://127.0.0.1:8000/admin/ 进入管理后台（需要超级管理员账号）

## 目录结构

```
jens_blog/             # 项目主目录
  ├── blog/            # 博客应用
  │    ├── migrations/  # 数据库迁移文件
  │    ├── templates/   # 模板文件
  │    ├── templatetags/ # 自定义模板标签
  │    ├── admin.py     # 后台管理配置
  │    ├── forms.py     # 表单定义
  │    ├── models.py    # 数据模型
  │    ├── urls.py      # URL配置
  │    └── views.py     # 视图函数
  ├── jens_blog/        # 项目设置
  │    ├── settings.py  # 项目设置
  │    ├── urls.py      # 主URL配置
  │    └── wsgi.py      # WSGI配置
  ├── static/           # 静态文件
  │    └── css/         # CSS样式
  ├── media/            # 用户上传的文件
  ├── manage.py         # Django管理脚本
  └── README.md         # 项目说明
``` 