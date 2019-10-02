import socket
import threading


class Cli:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self, range_start, range_stop):
        t = threading.Thread(target=self.send, args=(range_start, range_stop))
        t.start()  # 启动线程

    def send(self, range_start, range_stop):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        for data in [str(i).encode('utf-8') for i in range(range_start, range_stop)]:
            s.send(data)
            # 打印从服务端返回的数据：
            print((range_start, range_stop), s.recv(1024).decode('utf-8'))
        # s.send(b'exit')
        s.close()


if __name__ == '__main__':
    for port in range(10031, 10071):
        print('-------------', port)
        cli0 = Cli('127.0.0.1', port)
        cli1 = Cli('127.0.0.1', port)
        cli0.start(port, 100 + port)
        cli1.start(100 + port, 200 + port)


