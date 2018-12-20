import os
import tornado.ioloop
import tornado.httpserver
from application import Application

import config

if __name__ == "__main__":
    # 创建一个应用对象
    app = Application()
    # 启动服务
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options.get("port"))  # 绑定端口号
    httpServer.start()  # 如果传入的参数为None 或者小于等于0，开启对应cpu核心数个子进程

    tornado.ioloop.IOLoop.current().start()
