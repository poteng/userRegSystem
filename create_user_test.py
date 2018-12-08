import random
import database_command
import password_system

"""This script retrieves 10 users from the website, generates passwords for each user, and stores them into the 
database """

name_db = 'user_login.db'

# retrieve 10 user from https://randomuser.me/api/  generate password for each of them and insert
conn = database_command.create_connection(name_db)
for i in range(10):
    id_user = database_command.create_user(name_db)
    password = password_system.generate_password(random.randrange(6, 13), random.randrange(1, 5))
    database_command.update_password(conn, password, id_user)

conn.close()

