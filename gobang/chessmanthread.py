from chessman import *
import threading


# 根据开闭原则：对扩展开放，对修改关闭
# 要给ChessMan类添加多线程状态的功能，不要直接修改ChessMan类，而是写一个子类继承它
# 并在子类中添加相关的属性和方法
class ChessManThread(ChessMan):
    # 初始化
    def __init__(self):
        # 调用父类的初始化方法
        super().__init__()
        # 多线程的状态
        self.con = threading.Condition()

    # 通知下一个线程
    def do_notify(self):
        self.con.acquire()  # 先要acquire()获取状态才能进行wait()或notify()
        self.con.notify()
        self.con.release()

    # 等待上一个线程
    def do_wait(self):
        self.con.acquire()  # 先要acquire()获取状态才能进行wait()或notify()
        self.con.wait()
        self.con.release()
