from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# Pad data to be a multiple of 16 bytes (AES block size)
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + (chr(pad_len) * pad_len).encode()

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# Encrypt function
def encrypt_aes128(plaintext: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode()))
    return base64.b64encode(cipher.iv + ct_bytes).decode()

# Decrypt function
def decrypt_aes128(ciphertext_b64: str, key: bytes) -> str:
    data = base64.b64decode(ciphertext_b64)
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct)).decode()
