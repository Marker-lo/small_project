import tornado.web
import config

from views import index, login, sql, signIn


class Application(tornado.web.Application):
    # 创建路由映射
    def __init__(self):
        handlers = [
            (r"/", index.MainHandler),
            (r"/chat", index.chatHandler),
            (r"/login", index.loginHandler),
            (r"/signIn", signIn.signInHandler)
        ]
        # 调用父类的方法
        super(Application, self).__init__(handlers, **config.settings)
        # 连接数据库 在配置文件中引入参数
        self.db = sql.gecMysql(config.mysql['host'], config.mysql['user'], config.mysql['passwd'],
                               config.mysql['dbName'])
