import socket
import struct
import protocol
from threading import *


def recv_msg(conn):
    data_size = conn.protocol.recvall(conn, 4)
    length = struct.unpack('>I', data_size)[0]
    data_recv = conn.protocol.recvall(conn, length)
    #   lengthdict = len(protocol.parse_header(data_recv))
    data_recv = protocol.parse_header(data_recv)
    match data_recv["operation"]:
        case 2:
            recv_file(data_recv)
        case 1:
            recv_req(data_recv)
        case _:
            pass

    # need to add the recv


def recv_file(data_recv):
    return data_recv["msg"], data_recv["operation"]


def recv_req(data_recv):
    return data_recv["msg"], data_recv["operation"]


def send_data(conn, data, operation):
    if operation == 1:
        data = protocol.create_string_header(data)
        conn.sendall(data)
    elif operation == 2:
        data = protocol.create_file_header(data)
        conn.sendall(data)


def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    file_to_send = "C:\\Users\\UserStud\\Downloads\\close-up-of-tulips-blooming-in-field-royalty-free-image-1584131603.jpg"
    with open(file_to_send, 'rb') as file:
        filedata = file.read()
        data = protocol.create_file_header(filedata, file_to_send)
        length = len(data)
        packed_length = struct.pack('>I', length)
        # Send the packed length over the socket
        client_socket.sendall(packed_length)
        client_socket.send(data)


if __name__ == "__main__":
    main()