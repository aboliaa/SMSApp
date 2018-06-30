import base64
import hashlib

from Crypto.Cipher import AES

from config import ENC_KEY, ENC_IV

def encrypt(s):
    aes = AES.new(ENC_KEY, AES.MODE_CFB, IV=ENC_IV)
    return base64.b64encode(hashlib.sha256(aes.encrypt(s)).digest())

def decrypt(s):
    aes = AES.new(ENC_KEY, AES.MODE_CFB, IV=ENC_IV)
    return aes.decrypt(base64.b64decode(s))
