import psycopg2
import os
from .sql import tables, drop_tables

class Databse():
    def __init__(self):
        self.db_name=os.getenv("DB_NAME", '')
        self.db_host=os.getenv("DB_HOST", '')
        self.db_user=os.getenv("DB_USER", '')
        self.db_password=os.getenv("DB_PASSWORD", '')
        self.conn=None
    
    def connection_to_Databse(self):
        try:
            self.conn = psycopg2.connect(
                database=self.db_name,
                host=self.db_host,
                user=self.db_user,
                password=self.db_password
            )
        except Exception as e:
            print(e, "cannot connect to database")
        try:
            self.conn = psycopg2.connect(
                os.environ['DATABASE_URL'], sslmode='require')
        except Exception:
            pass

        return self.conn
    
    def create_tables(self):
        try:
            cursor = self.connection_to_Databse().cursor()
            for table in tables:
                cursor.execute(table)
        except Exception as e:
            print(e, "cannot execute")
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        cursor = self.connection_to_Databse().cursor()

        for query in drop_tables:
            cursor.execute(query)
        self.conn.commit()
        self.conn.close()
