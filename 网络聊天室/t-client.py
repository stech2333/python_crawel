import socket
import threading
import tkinter as tk
from tkinter import Listbox, Text, Scrollbar, Entry, Button, END

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888

class ChatApp:
    def __init__(self, root, username, port):
        self.root = root
        self.root.title("Chat Application")

        # 用户列表
        self.user_list = Listbox(root)
        self.user_list.bind('<Double-1>', self.start_private_chat)
        self.user_list.pack(side=tk.LEFT, fill=tk.BOTH)

        # 聊天内容显示区
        self.chat_display = Text(root, state='disabled')
        self.chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 消息输入区
        self.message_input = Entry(root)
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 发送按钮
        self.send_button = Button(root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind(('127.0.0.1', port))
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
        self.client_socket.sendall(username.encode("utf-8"))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        self.private_chat_user = None

    def start_private_chat(self, event):
        selected_user = self.user_list.get(self.user_list.curselection())
        if self.private_chat_user == selected_user:
            self.private_chat_user = None
        else:
            self.private_chat_user = selected_user

    def send_message(self):
        message = self.message_input.get()
        if self.private_chat_user:
            message = f"PRIVATE_CHAT:{self.private_chat_user}:{message}"
        self.client_socket.sendall(message.encode("utf-8"))
        self.message_input.delete(0, END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message.startswith("CLIENT_LIST:"):
                    client_list = message.split(":")[1]
                    self.user_list.delete(0, END)
                    for client in client_list.split(","):
                        self.user_list.insert(END, client)
                elif message.startswith("PRIVATE_CHAT:"):
                    sender, private_message = message.split(":")[1:]
                    if sender == self.private_chat_user:
                        self.chat_display.config(state='normal')
                        self.chat_display.insert(END, f"Private chat with {sender}: {private_message}\n")
                        self.chat_display.config(state='disabled')
                else:
                    self.chat_display.config(state='normal')
                    self.chat_display.insert(END, message + '\n')
                    self.chat_display.config(state='disabled')
            except:
                print("An error occurred while receiving messages.")
                self.client_socket.close()
                break

if __name__ == "__main__":
    username = input("Enter your username: ")
    port = int(input("Enter your port number: "))

    root = tk.Tk()
    ChatApp(root, username, port)
    root.mainloop()