# Writer: Leo
# @Time: 2018/10/28 10:59
"""用select实现服务端"""
import socket
import select
import datetime
import threading


# from Thread_handler import Thread_handler
class Thread_handler(threading.Thread):
    def __init__(self, data, conn, filename, in_, out_):
        super().__init__()
        self.data = data
        self.conn = conn
        self.filename = filename
        self.in_ = in_
        self.out_ = out_

    # 处理
    def run(self):
        now = datetime.datetime.now()
        self.out_.append(self.conn)
        with open(self.filename[self.conn], 'a', encoding='utf-8') as f:
            f.write(str(now) + '   message-->   ' + str(self.data) + '\n')
        print('已保存')

    def __del__(self):
        if self.data == None:
            self.conn.close()


def select_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口号
    server.bind(('192.168.1.147', 8080))
    # 设置监听
    server.listen(1024)

    in_ = [server, ]
    out_ = []
    other_ = []
    filename = {}

    while True:
        r_list, w_list, errmsg = select.select(in_, out_, other_, 1)
        for conn in r_list:
            if conn == server:
                client, info = conn.accept()  # 等待客户端连接
                # 记录客户端连接的时间
                connection_time = datetime.datetime.now()
                in_.append(client)  # 把客户端对象加到 in_ 列表
                str_ = str(info[0]) + '_' + str(info[1]) + '.log'
                filename[client] = str_  # 组成文件名存入字典
                # 写入文件中
                with open(str(filename[client]), 'a', encoding='utf8') as f:
                    f.write('连接时间：' + str(connection_time) + '\n')
            else:
                data = conn.recv(1024)  # 接收客户端消息
                print(data)
                # print(data)
                # now = datetime.datetime.now()
                # if data:  # 如果有数据
                #     out_.append(conn)  # 把用户加入到out_里触发select第二个参数
                #     # 将数据写入日志文件中
                #     with open(str(filename[conn]), 'a', encoding='utf8') as f:
                #         f.write(str(now) + '    message-->   ' + data + '\n')
                # else:
                #     in_.remove(conn)  # 没有数据 把客户端文件描述符从in_列表中删除
                if data:
                    t = Thread_handler(data, conn, filename, in_, out_)
                    t.start()
                else:
                    # 记录断开连接的时间
                    disconnection_time = datetime.datetime.now()
                    # 写入文件
                    with open(str(filename[conn]), 'a', encoding='utf8') as f:
                        f.write('断开时间：' + str(disconnection_time) + '\n')
                    in_.remove(conn)
                    del filename[conn]


if __name__ == '__main__':
    select_server()
