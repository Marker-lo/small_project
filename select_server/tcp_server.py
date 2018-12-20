# Writer: Leo
# @Time: 2018/8/15 20:21
"""服务端"""
import socket

# 创建一个数据流套接字 用于TCP传输
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口号
server_socket.bind(('', 8089))
# 监听
server_socket.listen(5)
# 接收客户端的连接
client_socket, client_info = server_socket.accept()
# 使用客户端的socket进行数据的发送与接收
rec_data = client_socket.recv(1024)
print(rec_data.decode('utf-8'))
# 给客户端回一条消息
msg = '你好'
client_socket.send(msg.encode('utf-8'))
# 关闭
server_socket.close()
