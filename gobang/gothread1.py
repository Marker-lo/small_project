import threading
import socket


# 用户下棋的线程
class UserGoThread(threading.Thread):
    def __init__(self, engine, chessman_pc, client_socket):
        super().__init__()
        self.engine = engine
        self.chessman_pc = chessman_pc
        self.client_socket = client_socket

    # 执行子线程的代码
    def run(self):
        while True:
            # 接收对方下棋坐标
            recv_data = self.client_socket.recv(1024).decode('utf-8')
            print('对方下棋位置：', recv_data)
            self.engine.parse_user_input(recv_data, self.chessman_pc)

            # 2 用户notify
            self.chessman_pc.do_notify()

            # 3 用户wait
            self.chessman_pc.do_wait()


# 电脑下棋的线程
class ComputerGoThread(threading.Thread):
    def __init__(self, engine, chessman_user, client_socket):
        super().__init__()
        self.engine = engine
        self.chessman_user = chessman_user
        self.client_socket = client_socket

    # 执行子线程的代码
    def run(self):
        while True:
            # 1 对方wait
            self.chessman_user.do_wait()

            # 下棋
            print('请下棋')
            user_input = input('> ')
            self.engine.parse_user_input(user_input, self.chessman_user)
            # 给对方发送消息
            self.client_socket.send(user_input.encode('utf-8'))

            # 3 对方notify
            self.chessman_user.do_notify()
