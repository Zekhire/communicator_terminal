import threading
import socket
import time
import struct


class Client(object):
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)                        # adres IP servera oraz port na ktorym odbedzie sie komunikacja

        try:                                                            # nawiazanie polaczenia z serwerem jesli jest on aktywny
            self.sock.connect(server_address)
            print('Connected with server ' + str(server_address[0]) + '!')
            self.communication()                                        # rozpoczecie dwukierunkowej komunikacji
        except socket.error:                                            # w przeciwnym razie koniec programu
            print('Run server', server_address[0], 'in order to connect!')


    def send_image(self, path):
        # try:
            image = open(path, "rb")
            data = "@image"
            data = data.encode('utf-8')
            self.sock.sendall(data)
            self.sock.sendall(image)
            image.close()
        # except:
        #     print("Error with image sending!")
        #     pass


    def recv_image(self):
        try:
            data = self.sock.recv(2**15)
            image = open("test.jpg", "wb")
            image.write(data)
            image.close()
        except:
            pass


    def send_data(self):
        print("Running!")
        while True:                                                     # nieskonczona petla ktora w oddzielnym watku wysyla dane sterujace robotem
            try:
                data = input()                                          # wczytanie danych
                if str(data)[:len("@send_image")] == "@send_image":
                    path = data[len("@send_image"):].split()[0]
                    self.send_image(path)
                    continue

                data = data.encode('utf-8')                             # kodowanie do odpowiedniego formatu

                # data =  12.421
                # data = bytearray(struct.pack("f", data)) 
                self.sock.sendall(data)                                 # wyslanie danych
            except socket.error:                                        # w przypadku bledu zakoncz wysylanie danych
                print('Disconnected with server!')
                break


    def receive_data(self):
        print("Running!")
        while True:                                                     # nieskonczona petla ktora w oddzielnym watku wysyla dane sterujace robotem
            try:
                data = self.sock.recv(2**15)
                if data.decode('utf-8') == "@image":
                    recv_image(self)

                print(data.decode('utf-8'))                       # dekodowanie do odpowiedniego formatu
            except socket.error:                                        # w przypadku bledu zakoncz wysylanie danych
                print('Disconnected with server!')
                break


    def communication(self):
        send_thread    = threading.Thread(target=self.send_data)        # watki odpowiedzialne za odbior i nadawanie danych
        send_thread.start()                                             # uruchomienie watkow

        recv_thread    = threading.Thread(target=self.receive_data)        # watki odpowiedzialne za odbior i nadawanie danych
        recv_thread.start()                                             # uruchomienie watkow


if __name__ == "__main__":
    client = Client(ip="192.168.1.105", port=50001)
