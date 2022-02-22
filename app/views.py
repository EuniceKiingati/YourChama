from flask import Flask, jsonify, request, abort, render_template, make_response
import json
from .models.user_models import User, Databse

def create_app():
    app=Flask(__name__)

    db = Databse()
    db.create_tables()

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/app/views/users/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        new_user= User(data)
        new_user.save()

        userobj= User()
        userlist=userobj.get_all_User()
        for user in userlist:
            del user['password']
            if user['username']==data['username']:
                response=jsonify({
                "message":"account created successfully",
                "status":201,
                "data": "user"
                })
                response.status_code= 201
                return response

    @app.route('/app/views/users/login', methods=['POST'])
    def login():
        data=request.get_json()
        user_obj=User()
        userlist=user_obj.get_all_User()
        
        username=data['username'].strip()
        password=data['password'].strip()
        
        for user in userlist:
            if user['username']== username and user['password']==password:
                return make_response (

                 jsonify({
                    "message":"login successful"
                }), 200)

        return make_response (jsonify({

            'status':"failed",
            'message':'no such user found, check logins'
        }), 404)





        
    return app