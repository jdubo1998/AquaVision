import threading
import socket as Socket
import re
import os

class SocketServerThread:
    code = None
    host = ''
    port = 0
    socket = None
    conn = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)

        self.socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(Socket.IPPROTO_TCP, Socket.TCP_KEEPIDLE, 1)
        self.socket.setsockopt(Socket.IPPROTO_TCP, Socket.TCP_KEEPINTVL, 20)
        self.socket.setsockopt(Socket.IPPROTO_TCP, Socket.TCP_KEEPCNT, 5)

        try:
            self.socket.bind((self.host, self.port))
        except:
            self.socket.shutdown(Socket.SHUT_RDWR)
            self.socket.close()
            print("Exception.")
        # except Socket.error as error:
        #     if error == errno.ECONNREFUSED:
        #         print(os.strerror(error.errno))
        #     else:
        #         raise

    def listen(self):
        try:
            self.socket.listen(1)
            print("D/SocketServerThread: Waiting for a conn.")
            self.conn, address = self.socket.accept()
            self.conn.settimeout(10)
            print("D/SocketServerThread: Connected to: " + address[0] + ":" + str(address[1]))

            threading.Thread(target = self.listenToconn).start()
        except KeyboardInterrupt :
            self.socket.shutdown(Socket.SHUT_RDWR)
            self.socket.close()
            os._exit(0)

    def listenToconn(self):
        size = 1024
        while True:
            message = input('Message: ')
            self.sendMessage(message)

            # try:
            #     print("Waiting for response...")
            #     data = self.conn.recv(size)
            #     print("Received repsonse: ")
            #     if data:
            #         message = data.decode('utf-8')
            #         message = re.sub("\n", "", message)

            #         print('D/SocketServerThread: Received: ' + message)

            #         if re.search("exit", message):
            #             self.conn.shutdown(Socket.SHUT_RDWR)
            #             self.conn.close()
            #             break
            #     else:
            #         raise Socket.error('Connection disconnected')
            # except:
            #     self.conn.close()
            #     return False

    def sendMessage(self, message):
        # if (self.isConnected):
        message += '\n'
        print('D/SocketServerThread: Sending: {}'.format(message))
        self.conn.sendall(str.encode(message))

    def closeSocket(self):
        self.socket.close()

if __name__ == "__main__":
    socket = SocketServerThread('', 50422)
    socket.listen()