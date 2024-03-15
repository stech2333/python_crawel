import socket
from threading import Thread
import sys
import os


def send_msg(sk):
    send_context = input("请输入信息：")
    send_ip = input("输入要发送的ip:")
    send_port = int(input("发送端口："))
    sk.sendto(send_context.encode("utf-8"),(send_ip,send_port))
    

def rec_msg(sk):
    rec_content,client_info = sk.recvfrom(1024)
    print(" ip:{}({}):{} ".format(client_info[0],client_info[1],rec_content.decode("utf-8")))
        
def main():  
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
    s.bind(("",7096))
    while True:
        op = input("要进行的操作：")
        if op == "1":
            send_msg(s)
        elif op == "2":
            rec_msg(s)
        else:
            break

    s.close()
            
    
if __name__ == "__main__":
    main()
