import socket
from threading import Thread
import sys
import os

class Friends:
    def __init__(self,name,ip,port):
        self.name = name
        self.ip = ip
        self.port = port
    def speak(self):
        print("My name is {}\n".format(self.name))

def add_friend(myfriend):
    name = input("请输入好友姓名：")
    ip = input("请输入好友的ip：")
    port = int(input("请输入与好友的端口："))
    x = Friends(name,ip,port)
    myfriend.append(x)
    print("{}添加成功".format(name))

def send_msg(sk,fri):
    send_context = input("请输入信息：")
    fri_name = input("请输入想要联系的好友：")
    try:
        flag = 0
        for person in fri:
            if person.name == fri_name:
                flag = 1
                send_ip = person.ip
                send_port = person.port
                sk.sendto(send_context.encode("utf-8"),(send_ip,send_port))
        if flag == 0:
            print("不存在该好友")
    except:
        pass

        

def rec_msg(sk):
    rec_content,client_info = sk.recvfrom(1024)
    print(" ip:{}({}):{} ".format(client_info[0],client_info[1],rec_content.decode("utf-8")))
        
def main(fri):  
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
    s.bind(("",7088))
    while True:
        op = input("要进行的操作：")
        if op == "1":
            send_msg(s,fri)
        elif op == "2":
            rec_msg(s)
        else:
            break

    s.close()
            
    
if __name__ == "__main__":
    my_Friend = []
    add_friend(my_Friend)

    main(my_Friend)
