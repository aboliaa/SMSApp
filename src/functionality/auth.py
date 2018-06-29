 # For performance, one should not use sqlite in production.
# This is only for demo.
import sqlite3
import base64
import hashlib

from Crypto.Cipher import AES

from models.db import SqlDB
from config import ENC_KEY, ENC_IV

def encrypt(s):
    aes = AES.new(ENC_KEY, AES.MODE_CFB, IV=ENC_IV)
    return base64.b64encode(hashlib.sha256(aes.encrypt(s)).digest())

def decrypt(s):
    aes = AES.new(ENC_KEY, AES.MODE_CFB, IV=ENC_IV)
    return aes.decrypt(base64.b64decode(s))


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    db = SqlDB()
    user = db.get_user_by_username(username)
    if not user or len(user) < 4:
        return False
    passwd = user[3]
    if encrypt(password) != passwd:
        return False
    return True
