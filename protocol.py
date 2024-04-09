import base64
import os
import msgpack


def recvall(sock, size):
    data = b''
    while len(data) < size:
        remaining_size = size - len(data)
        chunk = sock.recv(remaining_size)
        if not chunk:
            # Connection closed or error occurred
            break
        data += chunk
    return data


def create_string_header(msg):
    hdict = {"operation": "1",
             "length": str(len(msg)).zfill(8),
             "msg": msg
             }
    return msgpack.packb(hdict)


def create_file_header(msg, filepath):
    try:
        hdict = {"operation": "2",
                 "msg": msg,
                 "file_path": filepath
                 }
        return msgpack.packb(hdict)
    except Exception as e:
        print(e)
        return e


def parse_header(mbin):
    # Now, decode the accumulated_data
    hdict = msgpack.unpackb(mbin)
    return hdict

