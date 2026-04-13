#!/usr/bin/env python3
import socket

HOST = '127.0.0.1'  # Change to remote IP if needed
PORT = 65432

while True:
    msg = input("[GCS SEND] Type your message: ")
    if msg.lower() in ("exit", "quit"):
        print("Exiting sender.")
        break
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(msg.encode())
            data = s.recv(1024)
            print(f"[GCS RESPONSE]: {data.decode()}")
        except ConnectionRefusedError:
            print("Failed to connect to listener. Is it running?")
