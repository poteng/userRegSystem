# userRegSystem

It's a program to request user information from [randomuser.me] (https://randomuser.me/api/), and store information in a local SQLite database.

## Example

This example retrieves 10 users from the website, generates passwords with random complexities/lengths for each user, and stores them into the database

    name_db = 'user_login.db'
    conn = database_command.create_connection(name_db)
    
    for i in range(20):
        id_user = database_command.create_user(name_db)
        password = password_system.generate_password(random.randrange(6, 13), random.randrange(1, 5))
        database_command.update_password(conn, password, id_user)
    
    conn.close()

## Installation
Run this command to install Requests:

    pip install requests


## File

[create_user_test.py] (create_user_test.py) has basic example of how to use 
    
[database_command.py] (database_command.py) has commands for database manipulation.

[password_system.py] (password_system.py) has functions for generating/validating password

[test_check_password_level.py] (test_check_password_level.py) has unit test for `check_password()` function