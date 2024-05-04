import sqlite3

class DB():
    def __init__(self, db_name: str) -> None:
        self.conn = sqlite3.connect(f'bot_for_curses/databases/{db_name}.db')
        self.cursor = self.conn.cursor()


    def new_user(self, user_id, name, surname):
        self.cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
        result = self.cursor.fetchone()
        if result:
            pass
        else:
            self.cursor.execute('INSERT INTO users (id, name, surname, reffs) VALUES (?, ?, ?, 0)', (user_id, name, surname))


    def check_profile(self, user_id):
        self.name = self.cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
        result = self.cursor.fetchall()

        self.name = result[0][2]
        self.surname = result[0][3]
        self.reffs = result[0][4]


    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()



# conn = sqlite3.connect(r'bot_for_curses/databases/user.db')
# cursor = conn.cursor()

# # cursor.execute('''
# #                CREATE TABLE users(
# #                counter INTEGER PRIMARY KEY,
# #                id INT,
# #                name TEXT,
# #                surname TEXT,
# #                reffs INT
# #                )
# #                ''')

# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())



# cursor.execute(f'SELECT * FROM users WHERE id = {1108204259}')
# result = cursor.fetchall()

# name = result[0][4]
# print(name)

