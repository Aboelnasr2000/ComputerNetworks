# echo-client.py

import socket
import re
import base64

from PIL import Image
import cv2
# HOST = "127.0.0.1"  # The server's hostname or IP address
import sys
import time

FORMAT = 'utf-8'

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
ADDR = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)
Map = {1: 1}


def cache_st(name, content):
    Map[name] = content


def send_func(msg):
    client_send = re.split('\n', msg)
    for client_fun in client_send:
        client_function = re.split(" ", client_fun)
        if client_function[0] == "Disconnect":
            s.send(client_fun.encode())
            break

        message = client_fun

        print(f"[CLIENT] Command  : {message}")
        print(f"[CLIENT] File : {client_function[1]}")

        # print(Map)

        if client_fun in Map:
            print("\nFROM CACHE.............\n")
            print(Map[client_fun].decode(FORMAT) + "\n\n")
            continue
        print("\nFIRST TIME...............\n")
        if client_function[0] == "POST":
            data = send_file(client_function)
            message = message + "\r\n\r\n"
            message = message + data
            s.send(message.encode(FORMAT))
            print("Command Sent\n")
            response = s.recv(1024).decode(FORMAT)
            print(response + "\n\n")
            cache_st(client_fun, response.encode(FORMAT))
        elif client_function[0] == "GET":
            message = message
            s.send(message.encode(FORMAT))
            print("Command Sent\n")
            print("Data Received ..... \n")
            data = s.recv(4096).decode(FORMAT)
            cache_st(client_fun, data.encode(FORMAT))
            print(data + "\n\n")


def file_open(Filename):
    f = open(Filename, mode='r', encoding='utf-8')
    data_read = f.read()
    send_func(data_read)
    f.close()


def send_file(client_send):
    file_name = client_send[1]
    if ".png" in file_name:
        f = open("Light.png", mode='rb')
        data_read = f.read()
        f.close()
        return data_read
    else:
        f = open(file_name, mode='r', encoding='utf-8')
        data_read = f.read()
        f.close()
        return data_read


try:
    Filename = sys.argv[1]
except:
    Filename = "TestCases.txt"
file_open(Filename)
# print("Input Command")
# send_func(input())
