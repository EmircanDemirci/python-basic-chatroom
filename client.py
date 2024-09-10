import socket
import select
import sys
import threading

# Sunucuya bağlan
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv)!=3:
    print("./client.py <ip-address> <port-number>")
    exit()
ip_addr = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip_addr , port))


# Kullanıcı girişini dinleyen fonksiyon
def send_messages():
    while True:  # Kullanıcıdan sürekli mesaj al
        message = sys.stdin.readline()  # Kullanıcıdan mesaj al
        server.send(message.encode('utf-8'))  # Mesajı sunucuya gönder
        sys.stdout.write("<You> ")
        sys.stdout.write(message)
        sys.stdout.flush()


# Mesajları göndermek için ayrı bir thread başlat
send_thread = threading.Thread(target=send_messages)
send_thread.start()

# Sunucudan gelen mesajları dinleyen ana döngü

while True:
    sockets_list = [server]

    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if not message:
                print("Connection lost.")
                exit()
            else:
                print(message.decode('utf-8'))  # Sunucudan gelen mesaj
server.close()
conn.close()