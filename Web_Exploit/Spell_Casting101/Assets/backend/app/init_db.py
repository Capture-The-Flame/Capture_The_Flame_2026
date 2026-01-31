# this is code for actually initializing the local database, you will have to run this file with the command:
# python init_db.py 
# in the terminal every time you want to re-initialize the db so that you get the actual .db file.
# if you have a database.db file you don't have to do this

import sqlite3

connection = sqlite3.connect('database.db')

# To set up the sqlite database
with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()