import sqlite3
from sqlite3.dbapi2 import Connection
import requests


def create_user(db_path: str) -> int:
    """Retrieve a random user from https://randomuser.me/api/
    and persist the user (full name and email) into the given SQLite db

    :param db_path: path of the SQLite db file (to do: sqlite3.connect(db_path))
    :return: None
    """
    # get object using requests
    url = 'https://randomuser.me/api/'
    r = requests.get(url)

    # prevent failed response
    if r.status_code != requests.codes.ok:
        print('Failed response.')
        return - 1

    # extract first name, last name, and email
    data = r.json()
    first_name = data['results'][0]['name']['first']
    last_name = data['results'][0]['name']['last']
    full_name = first_name + ' ' + last_name
    email = data['results'][0]['email']

    # the unique id will be assigned automatically by the database engine
    sql_insert_user = """INSERT INTO users(full_name,first_name,last_name,email)
                        VALUES(?,?,?,?)"""

    # create connection to database
    conn = create_connection(db_path)
    create_user_table(conn)
    cursor = conn.cursor()
    cursor.execute(sql_insert_user, (full_name, first_name, last_name, email))
    conn.commit()

    # return id
    id_user = cursor.lastrowid

    conn.close()

    return id_user


def update_password(conn: Connection, password: str, id_user: int):
    """ insert password for a given id """
    sql_update_password = """ UPDATE users
                            SET password = ?
                            WHERE id = ? """
    cursor = conn.cursor()
    cursor.execute(sql_update_password, (password, id_user))
    conn.commit()
    return


def create_connection(db_path: str):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def create_user_table(conn: Connection):
    """ create table for full name, first name, last name, and email """
    sql_create_table = """  CREATE TABLE IF NOT EXISTS users (
                            id integer PRIMARY KEY,
                            full_name text NOT NULL,
                            first_name text NOT NULL,
                            last_name text NOT NULL,
                            email text NOT NULL,
                            password text
                            ); """
    cursor = conn.cursor()
    cursor.execute(sql_create_table)
    return


def show_user_table(db_path: str):
    """ print the content of user table from given database for checking purposes """
    sql_select_table = """SELECT full_name, email, password from  users;"""

    conn = create_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_select_table)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

