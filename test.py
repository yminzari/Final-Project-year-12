from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

class AESCipher:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, message):
        aes_cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        padded_plaintext = pad(message.encode(), AES.block_size)
        encrypted_message = aes_cipher.encrypt(padded_plaintext)
        return encrypted_message

    def decrypt(self, encrypted_message):
        aes_cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decrypted_data = aes_cipher.decrypt(encrypted_message)
        # Note: We don't decode here because we're expecting unpadded bytes
        return decrypted_data

# Example usage:
# Generate a random AES key with the appropriate length (e.g., 16 bytes for AES-128)
key = secrets.token_bytes(16)  # Change the argument to 24 or 32 for AES-192 or AES-256

# Use this key for encryption
iv = secrets.token_bytes(16)
cipher = AESCipher(key, iv)
encrypted = cipher.encrypt("Secret message")
print("Encrypted:", encrypted)
decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted.decode())  # Decode the decrypted bytes to get the string
