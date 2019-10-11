#!/usr/bin/env python

"""
author: ares
date: 2019/9/19
desc:
"""

import socket
import select

import queue

# Python 的 select() 函数是部署底层操作系统的直接接口。它监视着套接字，打开的文件和管道（任何调用 fileno() 方法后会返回有效文件描述符
# 的东西）直到它们变得可读可写或有错误发生。 select() 让我们同时监视多个连接变得简单，同时比在 Python 中使用套接字超时写轮询池要有效，
# 因为这些监视发生在操作系统网络层而不是在解释器层。

HOST = '127.0.0.1'
PORT = 8888

READ_ONLY = (
    select.POLLIN |
    select.POLLPRI |
    select.POLLHUP |
    select.POLLERR
)
READ_WRITE = READ_ONLY | select.POLLOUT
TIMEOUT = -1
MAX_CONN = 5

# 创建一个IPV4基于TCP协议的SOCKET对象
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定监听端口
server.bind((HOST, PORT))
# 等待连接的最大数量为5
server.listen(MAX_CONN)
# 设置非阻塞
server.setblocking(False)

# 获取epoll对象
# epoll = select.epoll()
poller = select.poll()

poller.register(server.fileno(), READ_ONLY)


print('waiting for connection...')


class ConnectionHandler(object):
    """connection handler"""
    def __init__(self, conn, poller):
        self.server_conn = conn
        self.poller = poller
        self.user_to_socket = {}
        self.socket_to_user = {}
        self.message_queues = {}
        # 存储socket对象的字典 {user: socket对象}
        self.fd_to_socket = {server.fileno(): server}

    def build(self):
        while True:
            events = poller.poll(TIMEOUT)

            for fd, flag in events:
                s = self.fd_to_socket[fd]

                # 处理 inputs
                if flag & (select.POLLIN | select.POLLPRI):
                    if s is server:
                        # 可读表示准备好接受新连接
                        connection, client_address = s.accept()
                        print('connection from ', client_address)
                        connection.setblocking(False)
                        self.fd_to_socket[connection.fileno()] = connection
                        poller.register(connection, READ_ONLY)

                        # 初始化一个发送数据的队列
                        self.message_queues[connection] = queue.Queue()
                    else:
                        data = s.recv(1024)
                        print(data)
                        if data:
                            sender, reciver, msg = str(data, encoding='utf-8').split(':')
                            self.user_to_socket.setdefault(sender, s)
                            self.socket_to_user.setdefault(s, sender)
                            # 可读的客户端套接字存在数据
                            print('received {!r} from user:{}'.format(data, sender))
                            if self.user_to_socket.get(reciver, None):
                                reciver_skt = self.user_to_socket[reciver]
                                self.message_queues[reciver_skt].put(bytes(msg, encoding='utf-8'))
                                # 添加输出通道以响应
                                poller.modify(reciver_skt, READ_WRITE)
                            else:
                                self.message_queues[s].put(bytes('`{}` is not online !!!'.format(reciver),
                                                                 encoding='utf-8'))
                                # 添加输出通道以响应
                                poller.modify(s, READ_WRITE)
                        else:
                            user = self.socket_to_user[s]

                            # 空的返回结果表示连接断开
                            print('closing', s.getpeername())
                            # 停止监听该连接的输入
                            poller.unregister(s)
                            s.close()

                            # 删除它的消息队列
                            del self.message_queues[s]
                            del self.socket_to_user[s]
                            del self.user_to_socket[user]

                elif flag & select.POLLHUP:
                    # 客户端挂起
                    print('closing', s.getpeername(), '(HUP)')
                    # 停止监听该连接输入
                    poller.unregister(s)
                    s.close()
                elif flag & select.POLLOUT:
                    # 套接字准备好发送任何数据
                    try:
                        next_msg = self.message_queues[s].get_nowait()
                    except queue.Empty:
                        # 无消息等待，所以我们停止检测
                        print(s.getpeername(), 'queue empty')
                        poller.modify(s, READ_ONLY)
                    else:
                        print('sending {!r} to user:{}'.format(next_msg, self.socket_to_user[s]))
                        s.send(next_msg)
                elif flag & select.POLLERR:
                    print('exception on', s.getpeername())
                    # 停止监听该连接的输入
                    poller.unregister(s)
                    s.close()

                    # 删除它的消息队列
                    del self.message_queues[s]








