import socket
import threading

HOST= '127.0.0.1'
PORT = 6084

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
display_names = []

#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{display_names[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            display_name = display_names[index]
            display_names.remove(display_name)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NAME".encode('utf-8'))
        display_name = client.recv(1024)


        display_names.append(display_name)
        clients.append(client)

        print(f"Display name of the client is {display_name}")
        broadcast(f"{display_name} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server running...")
receive()