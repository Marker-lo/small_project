import os

BASE_DIR = os.path.dirname(__file__)

# ���ö˿ں�
options = {
    "port": 8888
}

# ����templates��static·��
settings = {
    "template_path": os.path.join(BASE_DIR, "templates"),
    "static_path": os.path.join(BASE_DIR, "static"),
    "xsrf_cookies": False,  # ��վ����
    "login_url": "/login",  # �û���֤
    "cookie_secret": "hello"
}

# �������ݿ����
mysql = {
    "host": "127.0.0.1",
    "user": "root",
    "passwd": "123456",
    "dbName": "webchat"
}
