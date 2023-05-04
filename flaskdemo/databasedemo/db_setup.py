import sqlite3
connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()
create_table = "CREATE TABLE accounts (id int, username text)"
cursor.execute(create_table)
connection.commit()
connection.close()