from chessboard import *
from chessman import *
import random
import math


class Engine(object):
    # 初始化 需要把棋盘对象传入
    def __init__(self, chessboard):
        self.__chessboard = chessboard

    # 电脑下棋的策略
    # 告诉棋子的颜色 返回下棋的位置
    # 传入chessman对象的时候 把棋子的颜色写入
    # 该方法中负责填写棋子的位置
    def computer_go(self, chessman):
        if not isinstance(chessman, ChessMan):
            raise RuntimeError('类型不对 第1个参数必须为ChessMan对象')

        while True:
            # pos_x和pos_y在1~15之间随机生成一个数
            pos_x = math.ceil(random.random() * ChessBoard.board_size)  # [1,15]
            pos_y = random.randint(1, 15)
            if self.__chessboard.get_chess((pos_x, pos_y)) == '+':
                print('电脑下棋的位置:%d,%d' % (pos_x, pos_y))
                # 把pos_x和pos_y写入chessman对象中
                chessman.set_pos((pos_x, pos_y))
                # 退出while循环
                break

    # 用户在终端下棋
    # 提示用户 传入用户输入的字符串 并解释该字符串对应的位置
    # 传入chessman对象的时候 把棋子的颜色写入
    # 该方法中负责填写棋子的位置
    # 比如3,b 表示第3行第2列
    def parse_user_input(self, input, chessman):
        if not isinstance(chessman, ChessMan):
            raise RuntimeError('类型不对 第1个参数必须为ChessMan对象')

        ret = input.split(',')
        value1 = ret[0]  # '3'
        value2 = ret[1]  # 'b'
        # 转换成坐标
        pos_x = int(value1)
        pos_y = ord(value2) - ord('a') + 1
        # print(pos_y)
        chessman.set_pos((pos_x, pos_y))

    # 判断胜负
    # 当在pos位置放置color颜色的棋子后 胜负是否已分
    # 返回True表示胜负已分 返回False表示胜负未分
    def is_won(self, pos, color):
        # 垂直方向的判断
        start_x = 1
        if pos[0] - 4 >= 1:
            start_x = pos[0] - 4
        end_x = 15
        if pos[0] + 4 < 15:
            end_x = pos[0] + 4

        count = 0  # 统计有多少连续的棋子
        for pos_x in range(start_x, end_x + 1):
            if self.__chessboard.get_chess((pos_x, pos[1])) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                # 一但断开 统计计数清0 但不能退出
                count = 0

        # 水平方向
        start_y = 1
        if pos[1] - 4 >= 1:
            start_y = pos[1] - 4
        end_y = 15
        if pos[1] + 4 <= 15:
            end_y = pos[1] + 4

        count = 0  # 统计有多少连续的棋子
        for pos_y in range(start_y, end_y + 1):
            if self.__chessboard.get_chess((pos[0], pos_y)) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0

        # 左上右下方向
        start_x = 1
        if pos[0] - 4 >= 1:
            start_x = pos[0] - 4
        end_x = 15
        if pos[0] + 4 <= 15:
            end_x = pos[0] + 4

        start_y = 1
        if pos[1] - 4 >= 1:
            start_y = pos[1] - 4
        end_y = 15
        if pos[1] + 4 <= 15:
            end_y = pos[1] + 4

        count = 0
        ret = pos[0] - pos[1]
        for pos_x in range(start_x, end_x + 1):
            # for pos_y in range(start_y,end_y+1):
            pos_y = pos_x - ret
            if start_y <= pos_y <= end_y:
                if self.__chessboard.get_chess((pos_x, pos_y)) == color:
                    count += 1
                    if count >= 5:
                        return True
                else:
                    count = 0

        # 左下右上方向
        start_x = 1
        if pos[0] - 4 >= 1:
            start_x = pos[0] - 4
        end_x = 15
        if pos[0] + 4 <= 15:
            end_x = pos[0] + 4

        start_y = 1
        if pos[1] - 4 >= 1:
            start_y = pos[1] - 4
        end_y = 15
        if pos[1] + 4 <= 15:
            end_y = pos[1] + 4

        count = 0
        ret = pos[0] + pos[1]
        for pos_x in range(end_x, start_x - 1, -1):
            # for pos_y in range(start_y,end_y+1):
            pos_y = ret - pos_x
            if start_y <= pos_y <= end_y:
                if self.__chessboard.get_chess((pos_x, pos_y)) == color:
                    count += 1
                    if count >= 5:
                        return True
                else:
                    count = 0

        return False

    # 判断胜负
    # 判断chessman对象的棋子放置后 胜负是否已分
    # 调用is_won()并返回它的返回值即可
    def is_wonman(self, chessman):
        if not isinstance(chessman, ChessMan):
            raise RuntimeError('类型不对 第1个参数必须为ChessMan对象')
        pos = chessman.get_pos()
        color = chessman.get_color()
        return self.is_won(pos, color)

    # 游戏主流程
    def play(self):
        # 实现游戏的主要流程
        user_black = True  # True:用户选择黑棋 False:用户选择白棋 该值每盘棋变一次
        user_go = True  # True:当前轮到用户下 False:当前轮到电脑下 该值每步棋变一次

        while True:
            # 外循环 描述一盘棋

            # 1 用户选择先后
            print('请选择先后。b代表黑，w代表白:')
            user_input = input('> ')
            # if user_input[0] == 'b':
            if user_input.startswith('b'):  # 用户输入'b'
                user_black = True  # 用户选择黑棋
                user_go = True  # 第一步轮到用户下
            else:  # 用户输入'w'
                user_black = False  # 用户选择白棋
                user_go = False  # 第一步轮到电脑下

            # 2 初始化棋盘
            self.__chessboard.init_board()
            self.__chessboard.print_board()

            while True:
                # 内循环：描述一步棋
                chessman_user = ChessMan()
                chessman_pc = ChessMan()
                if user_black:
                    chessman_user.set_color('x')
                    chessman_pc.set_color('o')
                else:
                    chessman_user.set_color('o')
                    chessman_pc.set_color('x')

                # 3 判断是否轮到用户下
                if user_go:  # 轮到用户下
                    # 4.1 如果轮到用户下 则用户在终端输入x和y坐标
                    print('请下棋')
                    user_input = input('> ')
                    self.parse_user_input(user_input, chessman_user)
                    # parse_user_input()中会把坐标写入chessman_user对象
                    # TODO 万一用户输入的是非法字符串，囧么办？
                    self.__chessboard.set_chessman(chessman_user)
                else:  # 轮到电脑下
                    # 4.2 如果轮到电脑下 则随机选择空位下
                    self.computer_go(chessman_pc)
                    self.__chessboard.set_chessman(chessman_pc)

                # 打印棋盘
                self.__chessboard.print_board()

                # 5 判断是否赢棋
                if user_go:  # 轮到用户下
                    if self.is_wonman(chessman_user):
                        # 6.1 如果赢棋 退出内循环(break)
                        print('恭喜赢了')
                        break
                    else:
                        # 6.2 如果没有赢棋 则切换棋子 内循环继续
                        user_go = not user_go

                else:  # 轮到电脑下
                    if self.is_wonman(chessman_pc):
                        # 6.1 如果赢棋 退出内循环(break)
                        print('呵呵输了')
                        break
                    else:
                        # 6.2 如果没有赢棋 则切换棋子 内循环继续
                        user_go = not user_go

            # 7 判断是否继续游戏
            print('是否继续?(y/n)')
            user_input = input('> ')
            if user_input.startswith('y'):
                # 8.1 如果用户选择继续 则外循环继续
                pass
            else:
                # 8.2 如果用户选择退出 则退出外循环(break)
                break
