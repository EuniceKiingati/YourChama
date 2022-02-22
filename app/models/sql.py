from .import database_connection

tables=[
"""
CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY, 
    username varchar(30) not null UNIQUE,
    email varchar(50) not null UNIQUE, 
    password varchar(25) not null, 
    isadmin boolean not null
)

"""

]

drop_tables=[
    "DROP TABLE IF EXISTS  users CASCADE"

]

def select(table):
    db_obj = database_connection.Databse()
    conn = db_obj.connection_to_Databse()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(table))
    result = cursor.fetchall()
    conn.close()
    return result