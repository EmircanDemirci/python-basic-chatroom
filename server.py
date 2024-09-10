"""
server.py -- chatroom app
"""
import socket
import threading
import sys

def client_thread(conn, addr):
    conn.send("Welcome to the venroom!".encode('utf-8'))  # Karşı tarafa hoş geldin mesajı gönder
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')  # İstemciden mesaj al
            if not message:
                print(f"Connection lost: {addr}")
                break
            print(f"{addr} sent message: {message}")
            broadcast(message , conn)
        except:
            break
    conn.close()

"""
broadcast message to all clients
"""
def broadcast(msg , addr):
    for client in list_of_clients:
        if client!=addr:
            try:
                client.send(msg.encode("utf-8"))
            except:
                client.close()
                list_of_clients.remove(client)

# Sunucu socket'i oluştur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv)!=3:
    print("./server.py <ip-address> <port-number>")
    exit()
ip_addr = str(sys.argv[1])
port = int(sys.argv[2])
server.bind((ip_addr, port))
server.listen(5)


list_of_clients = []

print(f"Server started at ${ip_addr}:${port}")

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(f"Yeni bağlantı: {addr}")
    # Her istemci için ayrı bir thread başlat
    threading.Thread(target=client_thread, args=(conn, addr)).start()

server.close()
conn.close()