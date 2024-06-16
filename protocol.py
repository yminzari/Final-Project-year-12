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
        """
        encrypts the message
        :param message: the message
        :return: an encrypted message
        """
        try:
            aes_cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
            padded_plaintext = pad(message, AES.block_size)
            encrypted_message = aes_cipher.encrypt(padded_plaintext)
            return encrypted_message
        except Exception as e:
            print(e)

    def decrypt(self, encrypted_message):
        """
        decrypt the message
        :param encrypted_message: encrypted message
        :return: decrypted message
        """
        try:
            aes_cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
            decrypted_data = aes_cipher.decrypt(encrypted_message)
            decrypted_data = unpad(decrypted_data, AES.block_size)
            # Note: We don't decode here because we're expecting unpadded bytes
            return decrypted_data
        except Exception as e:
            print(e)


def recvall(sock, size):
    """
    receive all the data
    :param sock: socket
    :param size: the size to receive
    :return: the entire data
    """
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
    """
    creates a header for a string and then packs it with message pack
    :param msg: massage
    :return: packed message
    """
    hdict = {"operation": "1",
             "length": str(len(msg)).zfill(8),
             "msg": msg
             }
    return msgpack.packb(hdict)


def create_file_header(msg, filepath):
    """
    creates a header for a file and then packs it with message pack
    :param msg: message
    :param filepath: file path
    :return: packed message
    """
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
    """
    unpacks the message
    :param mbin: packed message
    :return: return unpacked message
    """
    # Now, decode the accumulated_data
    hdict = msgpack.unpackb(mbin)
    return hdict

