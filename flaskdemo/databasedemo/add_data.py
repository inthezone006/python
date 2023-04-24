import sqlite3

connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()
rahul = (1, 'inthezone006')
insert_query = "INSERT INTO accounts VALUES (?, ?)"
cursor.execute(insert_query, rahul)
connection.commit()
connection.close()