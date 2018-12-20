from chessboard import *
from chessman import *
from engine import *
from chessmanthread import *
from gothread1 import *
import socket


# 主流程
def main():
    # 自己实现
    chessboard = ChessBoard()
    # 创建Engine对象
    engine = Engine(chessboard)
    # 开始游戏
    engine.play()


# 多线程版本的主流程
def main_thread():
    # 创建棋盘对象 并初始化
    chessboard = ChessBoard()
    # 创建引擎对象 并传入棋盘对象作为参数
    engine = Engine(chessboard)
    # 创建两个ChessManThread对象
    chessman_user = ChessManThread()
    chessman_pc = ChessManThread()
    chessman_user.set_color('x')
    chessman_pc.set_color('o')

    # 创建一个数据流套接字，用于tcp传输
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.7', 10086))
    chessboard.init_board()
    chessboard.print_board()

    # 创建两个子线程 并启动
    t1 = ComputerGoThread(engine, chessman_pc, client_socket)
    t1.setDaemon(True)  # 设置为守护线程 这样主线程退出的时候子线程也跟着强制退出了
    t1.start()
    t2 = UserGoThread(engine, chessman_user, client_socket)
    t2.setDaemon(True)
    t2.start()

    while True:
        # 1 用户wait
        chessman_user.do_wait()

        # 2 在棋盘上摆放棋子
        chessboard.set_chessman(chessman_user)
        chessboard.print_board()
        if engine.is_wonman(chessman_user):
            print('呵呵输了')
            break

        # 3 电脑notify
        chessman_pc.do_notify()

        # 4 电脑wait
        chessman_pc.do_wait()

        # 5 在棋盘上摆放棋子
        chessboard.set_chessman(chessman_pc)
        chessboard.print_board()
        if engine.is_wonman(chessman_pc):
            print('恭喜赢了')
            break

        # 6 用户notify
        chessman_user.do_notify()


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # main()
    main_thread()
