# Writer: Leo
# @Time: 2018/8/15 20:21
"""客户端"""
import socket

# 创建一个数据流套接字 用于TCP传输
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务端
client_socket.connect(('192.168.0.131', 8089))
# 给服务端发送消息
msg = 'Yse'
client_socket.send(msg.encode('utf-8'))
# 接收服务端的消息
rec_data = client_socket.recv(1024)
print(rec_data.decode('utf-8'))
# 关闭
client_socket.close()
