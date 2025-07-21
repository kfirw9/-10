import socket
import struct
import threading
import time
import pyautogui
from io import BytesIO

def send(sock, data):
    sock.sendall(struct.pack('>I', len(data)) + data)

def keyboard():
    s = socket.socket()
    s.connect(('127.0.0.1', 9999))
    send(s, b'keyboard')
    while True:
        send(s, b"Key pressed")
        time.sleep(1)

def mouse():
    s = socket.socket()
    s.connect(('127.0.0.1', 9999))
    send(s, b'mouse')
    while True:
        x, y = pyautogui.position()
        msg = f"{x},{y}".encode()
        send(s, msg)
        time.sleep(1)

def screenshot():
    s = socket.socket()
    s.connect(('127.0.0.1', 9999))
    send(s, b'screenshot')
    while True:
        img = pyautogui.screenshot()
        with BytesIO() as f:
            img.save(f, format='PNG')
            send(s, f.getvalue())
        time.sleep(2)

def main():
    threading.Thread(target=keyboard).start()
    threading.Thread(target=mouse).start()
    threading.Thread(target=screenshot).start()

if __name__ == '__main__':
    main()
