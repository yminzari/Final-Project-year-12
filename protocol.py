import base64
import os
import msgpack
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, message):
        try:
            aes_cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
            padded_plaintext = pad(message, AES.block_size)
            encrypted_message = aes_cipher.encrypt(padded_plaintext)
            return encrypted_message
        except Exception as e:
            print(e)

    def decrypt(self, encrypted_message):
        try:
            aes_cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
            decrypted_data = aes_cipher.decrypt(encrypted_message)
            decrypted_data = unpad(decrypted_data, AES.block_size)
            # Note: We don't decode here because we're expecting unpadded bytes
            return decrypted_data
        except Exception as e:
            print(e)


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

