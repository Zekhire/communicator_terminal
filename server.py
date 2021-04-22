import socket
import threading
import struct
import argparse


class Server(object):
    def __init__(self, ip, port, n):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ip, port)                                # adres IP servera oraz port na ktorym odbedzie sie komunikacja
        self.sock.bind(self.server_address)                             # powiazanie socketa z adresem IP i odpowiednim portem
        self.sock.listen(n)                                             # uruchomienia nasluchiwania na przychadzace polaczenie
        self.client_addresses = []
        self.connections      = []
        self.receive_threads  = []
        self.start_communication(n)


    def send_data(self):
        while True:                                                     # nieskonczona petla ktora w oddzielnym watku wysyla dane sterujace robotem
            try:
                data = input()                                          # wczytanie danych
                data = data.encode('utf-8')                             # kodowanie do odpowiedniego formatu

                # data =  12.421
                # data = bytearray(struct.pack("f", data)) 
                for i in range(len(self.connections)):
                        self.connections[i].sendall(data)
            except socket.error:                                        # w przypadku bledu zakoncz wysylanie danych
                print('Disconnected with server!')
                break
            

    def receive_data(self, connection):
        while True:                                                     # nieskonczona petla odbierajaca dane
            try:
                data = connection.recv(2**15)                               # odebrane dane
                if data:
                    print(data.decode('utf-8'))                       # dekodowanie do odpowiedniego formatu
                    # data = struct.unpack("f", data)[0]
                    # print(data)                                     # dekodowanie do odpowiedniego formatu
                    for i in range(len(self.connections)):
                        if self.connections[i] != connection:
                            self.connections[i].sendall(data)
            
            except socket.error:
                connection.close()
                break


    def start_communication(self, n):
        for i in range(n):
            print('Waiting for connection')                                 # oczekiwanie na klienta i nawiazanie polaczenia
            connection, client_address = self.sock.accept()
            print('Connected with IP', client_address[0])
            self.connections.append(connection)
            self.client_addresses.append(client_address)

        for i in range(n):
            receive_thread = threading.Thread(target=self.receive_data, args=(self.connections[i],))
            receive_thread.start()
            self.receive_threads.append(receive_thread)

        send_thread = threading.Thread(target=self.send_data)
        send_thread.start()

        for i in range(n):
            self.receive_threads[i].join()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--clients", type=int, default=2, help="number of clients")
    args = vars(ap.parse_args())

    server = Server(ip="192.168.1.105", port=50001, n=args["clients"])
