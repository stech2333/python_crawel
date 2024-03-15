import socket
import threading

# 定义服务器地址和端口
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口
server_socket.bind((SERVER_HOST, SERVER_PORT))

# 监听连接
server_socket.listen()

# 用于存储客户端信息的字典
clients = {}

# 用于分配唯一标识符的计数器
client_id_counter = 1

# 发送消息给指定客户端
def send_message(client_socket, message):
    try:
        client_socket.sendall(message.encode("utf-8"))
    except:
        print("An error occurred while sending message.")

# 处理客户端消息
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    username = client_socket.recv(1024).decode("utf-8")
    clients[username] = client_socket
    print(f"Username '{username}' connected")
    broadcast_clients_list()

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message.startswith("PRIVATE_CHAT:"):
                parts = message.split(":")
                target_user = parts[1]
                private_message = parts[2]
                if target_user in clients:
                    send_message(clients[target_user], f"(Private) {username}: {private_message}")
                    send_message(client_socket,f"(Private) {username}: {private_message}")
                else:
                    send_message(client_socket, f"User '{target_user}' is not online.")
            else:
                broadcast_message(username, message)
        except:
            print(f"Connection with {username} closed")
            del clients[username]
            broadcast_clients_list()
            client_socket.close()
            break

# 广播消息给所有客户端
def broadcast_message(sender, message):
    for client in clients.values():
#        if client != clients[sender]:
        send_message(client, f"{sender}: {message}")

# 广播客户端列表
def broadcast_clients_list():
    client_list = "CLIENT_LIST:" + ",".join(clients.keys())
    for client in clients.values():
        send_message(client, client_list)

# 接受新连接
while True:
    client_socket, client_address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
