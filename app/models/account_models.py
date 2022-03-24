#from sqlite3 import dbapi2
#from unittest import result
from .database_connection import Databse
from .sql import select


class Account(Databse):
    def __init__(self, data=None):
        if data:
            self.account_type= data['account_type']
            self.balance= data['balance']
            self.user_id= data['user_id']
            
    
    def save(self):
        db_obj = Databse()
        self.conn = db_obj.connection_to_Databse()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO accounts(account_type,balance,user_id)\
            VALUES (%s, %s, %s)",
                       (self.account_type, self.balance, self.user_id))

        self.conn.commit()
        self.conn.close()
    
    def get_all_accounts(self):
        db_obj=Databse()
        self.conn=db_obj.connection_to_Databse()
        cursor=self.conn.cursor()
        cursor.execute("SELECT accounts.acc_id,accounts.account_type, accounts.balance, users.user_id\
        FROM users JOIN accounts ON users.user_id=accounts.user_id")

        result=cursor.fetchall()
        accountlist=[]
        
        for account in result:
            single_account = {}
            single_account['acc_id']=account[0]
            single_account['account_type'] = account[1]
            single_account['balance'] = account[2]
            single_account['user_id'] = account[3]
            accountlist.append(single_account)

        self.conn.close()
        return accountlist

    def delete_account(self, account_id):
        db_obj=Databse()
        self.conn=db_obj.connection_to_Databse()
        cursor=self.conn.cursor()
        
        try:
            cursor.execute(
            "DELETE FROM accounts WHERE acc_id=%s", (account_id)
        )
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()
    
    #def get_single_account(self, account_id):