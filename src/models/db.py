import sqlite3 # For performance, one should not use sqlite in production.

from utils.crypt import encrypt

class SqlDB(object):
    def __init__(self):
        self.db = sqlite3.connect('data/db-test')
        self.cursor = self.db.cursor()

    def get_user_by_username(self, username):
        self.cursor.execute(
            '''SELECT * FROM users WHERE username=?''',
            (username,)
        )
        user = self.cursor.fetchone()
        return user

    def commit(self):
        self.db.commit()

def populate_db():
    db_conn = SqlDB()

    db_conn.cursor.execute('''
        CREATE TABLE users(
        id INTEGER PRIMARY KEY, 
        name TEXT,
        username TEXT,
        password TEXT)'''
    )

    name = 'Test User'
    username = 'user'
    password = encrypt('secret')
    db_conn.cursor.execute(
        '''INSERT INTO users(name, username, password) VALUES(?,?,?)''',
        (name, username, password)
    )

    db_conn.commit()

if __name__ == '__main__':
    populate_db()