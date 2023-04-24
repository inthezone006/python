import sqlite3

connection = sqlite3.connect('accounts.db')
cursor = connection.Cursor()

create_table = "CREATE TABLE accounts (id int, username text, )"