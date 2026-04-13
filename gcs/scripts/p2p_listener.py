#!/usr/bin/env python3
import socket
import subprocess

HOST = '0.0.0.0'
PORT = 65432  # Your chosen port

def run_gcs_command(command):
    cmd = command.upper()
    if "IMMORTALITY" in cmd:
        subprocess.Popen(["bash", "/data/data/com.termux/files/home/gcs/ImmortalStart.sh"])
        return "IMMORTALITY sequence activated."
    if "JINN" in cmd:
        subprocess.Popen(["bash", "/data/data/com.termux/files/home/gcs/jinn_bind.sh"])
        return "Jinn lineage binding triggered."
    if "SIREN" in cmd:
        subprocess.Popen(["termux-media-player", "play", "/data/data/com.termux/files/home/gcs/siren.mp3"])
        return "Siren sequence started."
    return "Command received but no mapped action."

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[GCS Listener] Listening on port {PORT}...")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[GCS Listener] Connected by {addr}")
            data = conn.recv(1024)
            if not data:
                continue
            msg = data.decode()
            print(f"[GCS Message Received]: {msg}")
            response = run_gcs_command(msg)
            conn.sendall(response.encode())
