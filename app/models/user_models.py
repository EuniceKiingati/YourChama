from .database_connection import Databse
from werkzeug.security import generate_password_hash


class User(Databse):
    def __init__(self, data=None):
        if data:
            self.username=data.get('username',).strip()
            self.email=data['email'].strip()
            self.password=generate_password_hash(data['password'].strip())
            self.isadmin=data.get('isadmin', False)
            db_obj=Databse()
            self.conn=db_obj.connection_to_Databse()

    def save(self):

        try:
            db_obj = Databse()
            self.conn = db_obj.connection_to_Databse()
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users(username,email,password,isadmin)\
            VALUES (%s, %s, %s, %s)",
                           (self.username, self.email, self.password, self.isadmin))

            # cursor.execute(query)
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e, "could not save")
    
    def get_all_User(self):
        db_obj = Databse()
        self.conn = db_obj.connection_to_Databse()  # create connection to db
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        Userlist = []
        for user in result:

            single_user = {}
            single_user['user_id'] = user[0]
            single_user["username"] = user[1]
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user['isadmin'] = user[4]
            Userlist.append(single_user)
    

        self.conn.close()
        return Userlist

    def delete_user(self, user_id):
        db_obj = Databse()
        self.conn = db_obj.connection_to_Databse()
        cursor = self.conn.cursor()
        # delete a user
        try:
            cursor.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id, )
            )
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()
