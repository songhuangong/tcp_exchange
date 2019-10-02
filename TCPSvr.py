# 导入socket库
import socket
import threading
import time


class TCPSvr:
    def __init__(self, port):
        # 链接集合
        self.cli_list = []
        # 创建一个基于IPv4和TCP协议的socket
        self.svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定监听端口：（服务的端口号<1024时，需要管理员权限）
        self.svr.bind(('127.0.0.1', port))  # 我们写的不是标准服务(标准服务HTTP，STMP)
        # 开始监听：
        self.svr.listen(5)  # param : 等待连接的最大数量
        print('listen port {0} waiting for connecting'.format(port))

    def start(self):
        # 永久循环来接收来自客户端的连接：
        while True:
            print('set num:', len(self.cli_list))
            # 接收一个新的连接：
            cli, addr = self.svr.accept()  # accept会等待并发返回一个客户端的连接
            if len(self.cli_list) <= 1:
                self.cli_list.append(cli)
                if len(self.cli_list) == 2:
                    print("22222222222222222222222")
                    for t in self.cli_list:
                        print('t: ', t)
                    # 创建新线程（多线程）来处理这个连接：单线程在处理过程中，无法接收其他客户端的连接
                    # t = threading.Thread(target=tcp_link, args=(cli, addr))
                    t0 = threading.Thread(target=self.tcp_exchange, args=(0,))
                    t0.start()  # 启动线程
                    t1 = threading.Thread(target=self.tcp_exchange, args=(1,))
                    t1.start()  # 启动线程


    def tcp_exchange(self, index):
        """
        :param index:
        :return:
        接受0的数据发送给1，接受1的数据发送给0
        """
        # 永久循环接受数据
        while True:
            try:
                if len(self.cli_list) != 2:
                    continue
                cli = self.cli_list[index]
                # addr = cli.raddr
                data = cli.recv(1024)  # 接收来自客户端的数据，最大（1k）,阻塞式等待
                time.sleep(1)  # stop: 1s 避免过度占用CPU
                # 如果客户端没有发送数据或发送’exit‘：关闭连接
                if not data:
                    break
                # 发送编码后的数据：
                if index == 0:
                    self.cli_list[1].send(data)
                elif index == 1:
                    self.cli_list[0].send(data)
            except Exception as e:
                print("000", e)
                cli.close()
                if cli in self.cli_list:
                    print("关闭异常断开的")
                    self.cli_list.remove(cli)

        try:
            print("关闭正常断开的")
            cli.close()
            if cli in self.cli_list:
                self.cli_list.remove(cli)
        except Exception as e:
            print("111", e)
        # print('Connection from %s:%s closed' % addr)


# def tcp_link(cli, addr):  # 新线程执行的函数
#     print('Accept new connection from %s:%s...' % addr)
#     # cli.send('Welcome!'.encode('utf-8'))  # 发送数据给客户端
#     while True:
#         data = cli.recv(1024)  # 接收来自客户端的数据，最大（1k）,阻塞式等待
#         time.sleep(1)  # stop: 1s 避免过度占用CPU
#         # 如果客户端没有发送数据或发送’exit‘：关闭连接
#         if not data:
#             break
#         # 发送编码后的数据：
#         cli.send(('Hello, %s' % data.decode('utf-8')).encode('utf-8'))
#     cli.close()
#     print('Connection from %s:%s closed' % addr)

def start_one_tcp_svr(one_port):
    print(port)
    svr = TCPSvr(one_port)
    svr.start()


if __name__ == '__main__':
    for port in range(10031, 10071):
        t = threading.Thread(target=start_one_tcp_svr, args=(port,))
        t.start()




