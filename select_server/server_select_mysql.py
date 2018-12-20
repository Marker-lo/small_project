# Writer: Leo
# @Time: 2018/11/2 18:57
"""用select实现服务端"""
import socket
import select
import datetime
import threading
import pymysql


# from Thread_handler import Thread_handler
class Thread_handler(threading.Thread):
    def __init__(self, data, conn, filename, in_, out_, db, cursor):
        super().__init__()
        self.data = data
        self.conn = conn
        self.filename = filename
        self.in_ = in_
        self.out_ = out_
        self.db = db
        self.cursor = cursor

    # 处理
    def run(self):
        send_msg_time = datetime.datetime.now()
        self.out_.append(self.conn)
        message_ = str(send_msg_time) + '_' + str(self.data)
        print(message_)
        print(self.filename[self.conn])
        sql = 'SELECT message FROM logs WHERE '
        self.cursor.execute(sql)
        one = self.cursor.fetchone()
        print(one)
        if not one:
            sql = 'UPDATE logs SET message=%s WHERE flag=%s'
        else:
            sql = 'UPDATE logs SET message=message+%s WHERE flag=%s'
        try:
            self.cursor.execute(sql, (message_, self.filename[self.conn]))
            self.db.commit()
        except:
            self.db.rollback()
        print('已保存')

    def __del__(self):
        if self.data == None:
            self.conn.close()


def select_server():
    # 连接数据库
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='server_select_log')
    # 创建游标，操作数据库
    cursor = db.cursor()
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
                # 存入数据库
                ip = info[0]
                port = info[1]
                # 将ip和port作为一个联系值
                flag = ip + '_' + str(port)
                print(flag)
                filename[client] = flag
                sql = 'INSERT INTO logs(flag, ip, port, connection_time) values (%s, %s, %s, %s)'
                try:
                    cursor.execute(sql, (flag, ip, port, str(connection_time)))
                    db.commit()  # 事务处理
                except:
                    db.rollback()  # 执行数据回滚-->当sql语句执行失败时
            else:
                data = conn.recv(1024)  # 接收客户端消息
                print(data.decode())
                data = data.decode()
                if data:
                    t = Thread_handler(data, conn, filename, in_, out_, db, cursor)
                    t.start()
                else:
                    # 记录断开连接的时间
                    disconnection_time = datetime.datetime.now()
                    # 存入数据库
                    sql = 'UPDATE logs SET disconnection_time=%s WHERE flag=%s'
                    try:
                        cursor.execute(sql, (disconnection_time, filename[conn]))
                        db.commit()  # 事务处理
                    except:
                        db.rollback()  # 执行数据回滚
                    in_.remove(conn)
                    del filename[conn]


if __name__ == '__main__':
    select_server()
