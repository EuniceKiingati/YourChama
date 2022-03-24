from .import database_connection

tables=[
"""
CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY, 
    username varchar(30) not null UNIQUE,
    email varchar(50) not null UNIQUE, 
    password varchar(250) not null, 
    isadmin boolean not null
)

""", 
"""
CREATE TABLE IF NOT EXISTS accounts(
    acc_id serial PRIMARY KEY,
    user_id int REFERENCES users(user_id) not null,
    account_type varchar(30) not null,
    balance varchar(50) not null
) 
"""

]

drop_tables=[
    "DROP TABLE IF EXISTS  users CASCADE"
    "DROP TABLE IF EXISTS accounts CASCADE"

]

def select(table):
    db_obj = database_connection.Databse()
    conn = db_obj.connection_to_Databse()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(table))
    result = cursor.fetchall()
    conn.close()
    return result