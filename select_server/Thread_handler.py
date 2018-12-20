# Writer: Leo
# @Time: 2018/10/28 12:55
"""创建线程处理客户端消息"""
import threading
import datetime

'''
class Thread_handler(threading.Thread):
    def __init__(self, conn, filename, in_, out_):
        super().__init__()
        self.conn = conn
        self.filename = filename
        self.in_ = in_
        self.out_ = out_

    # 处理
    def run(self):
        data = self.conn.recv(1024).decode('utf-8')
        now = datetime.datetime.now()
        if data:
            self.out_.append(self.conn)
            with open(self.filename[self.conn], 'a', encoding='utf-8') as f:
                f.write(str(now) + '   message-->   ' + data + '\n')
            print('已保存')
        else:
            print(self.in_)
            if self.conn in self.in_:
                self.in_.remove(self.conn)
                del self.filename[self.conn]
            else:
                print('不存在于列表中')
'''


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
            f.write(str(now) + '   message-->   ' + self.data + '\n')
        print('已保存')

    def __del__(self):
        if self.data == None:
            self.conn.close()
