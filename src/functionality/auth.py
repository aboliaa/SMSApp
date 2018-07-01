from models.db import SqlDB
from utils.crypt import encrypt

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    It fetches username and password-hash from SQLite DB and
    compares them with input values.
    """
    db = SqlDB()
    user = db.get_user_by_username(username)
    if not user or len(user) < 4:
        return False
    passwd = user[3]
    if encrypt(password) != passwd:
        return False
    return True
