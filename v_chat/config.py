import os

BASE_DIR = os.path.dirname(__file__)

# 配置端口号
options = {
    "port": 8888
}

# 配置templates、static路径
settings = {
    "template_path": os.path.join(BASE_DIR, "templates"),
    "static_path": os.path.join(BASE_DIR, "static"),
    "xsrf_cookies": False,  # 跨站请求
    "login_url": "/login",  # 用户认证
    "cookie_secret": "hello"
}

# 配置数据库参数
mysql = {
    "host": "127.0.0.1",
    "user": "root",
    "passwd": "123456",
    "dbName": "webchat"
}
