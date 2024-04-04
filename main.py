from pytesseract import pytesseract
import gettext
import cv2
import numpy as np
import oracledb
import pickle
import struct
import socket
import oracledb

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = 'localhost'  # Change this to the IP address or hostname of your server
port = 12345
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

# Accept a connection from a client
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Function to receive an image from the client
def receive_image():
    # Receive the length of the incoming image
    data = b""
    payload_size = struct.calcsize(">L")
    while len(data) < payload_size:
        data += client_socket.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]

    # Receive the image data
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    img_data = data[:msg_size]
    data = data[msg_size:]

    # Unpickle and return the image
    img = pickle.loads(img_data)
    return img
# Receive the image from the client

received_image = receive_image()

# Close the sockets
client_socket.close()
server_socket.close()

#text = open("C:\\Users\\yminz\\Downloads\\check.txt", 'r', encoding='utf-8')
img = cv2.imread("C:\\Users\\yminz\\Downloads\\test_scan1.jpg")
text = pytesseract.image_to_string(received_image, 'Hebrew', config="--psm 1 ")
#text.replace("\\n", "")
text_dir = text.split(" ")
text_dir = text_dir[::-1]
print(text)
print(text_dir)
with open("test_write.txt", 'w', encoding='utf-8') as f:
    f.write(text)
    f.close()
i = 0
first_name = ""
id = ""
last_name = ""
phone = []
for txt in text_dir:
    text_dir[i].replace("\\n", "")
    text_dir[i].replace("n\\", "")
    if "r.n" in txt:
        id = text_dir[i-1]
        print(id)
    if "משפחה" in txt:
        last_name = text_dir[i-1]
    if "טלפון" in txt:
        ph = text_dir[i - 2]
        ph2 = ""
        for p in ph:
            if p.isnumeric():
                ph2 += p
        phone.append(ph2)
    if "טלעבודהגייה" in txt:
        ph = text_dir[i-1]
        ph2 = ""
        h = 1
        for p in ph:
            if p.isnumeric() and h < 11:
                ph2 += p
            h += 1
        phone.append(ph2)
    if "פרטי:" in txt:
        first_name = text_dir[i-1]
    i = i+1
id2 = ""
for let in id:
    if let.isnumeric():
        id2 += let
        id.replace(let, "")
id2 = f"תז: {id2}\n"
print(phone)
print(first_name)
with open("test_write2.txt", 'w', encoding='utf-8') as f:
    f.write(id2)
    f.write(f"שם משפחה: {last_name}\n")
    f.write(f"שם פרטי: {first_name}\n")
    for w in phone:
        f.write(f"טלפון: {w}\n")
#print(text.read())