from collections import UserList
from distutils.command.config import config
from urllib import response
from flask import Flask, jsonify, request, abort, render_template, make_response
import json
import datetime
import jwt
import os 
from functools import wraps
from werkzeug.security import check_password_hash

from app.models.account_models import Account
from .models.user_models import User, Databse


def bad_request(message):
    response = jsonify({
        "message": message,
        "status": 400,
    })
    response.status_code = 400
    return response

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']=os.getenv("SECRET_KEY")

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user1=User()
            users=user1.get_all_User()
            current_user= None
            if 'token' in request.headers:
                token=request.headers['token']
                if not token:
                    return jsonify({
                        'message':'token missing',
                        'status':401
                    })
                #verify token valid
                try:
                    data=jwt.decode(token, app.config['SECRET_KEY'])
                    for user in users:
                        if user['username']==data['username']:
                            current_user=user

                except:
                    return jsonify({
                        'message': 'token is invalid',
                        'status': 401
                    })

            return f(current_user, *args, **kwargs)
        return decorated
    
    
    
    
    
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
        #response={}
        #print(userlist, data)
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
            if user['username']== username:
                if  check_password_hash(user['password'], password):
                    token= jwt.encode({'username': data['username'], 'exp':datetime.datetime.utcnow()
                    + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
                    return make_response (

                    jsonify({
                        #making it a regular string
                        'token':token,
                        "message":"login successful"
                    }), 200)
            else:
                print(user['username'])

        return make_response (jsonify({

            'status':"failed",
            'message':'no such user found, check logins'
        }), 404)

    @app.route('/app/views/users/<int:user_id>', methods=['GET'])
    def get_single_user(user_id):
        single_user=User()
        userlist=single_user.get_all_User()
        for user in userlist:
            if user['user_id']==user_id:
                user_data = {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    #add remaining data
                }
                response=jsonify({
                "status":200,
                "data": user_data
                })
                response.status_code= 200
                return response
        response=jsonify({
            "message":"user not found",
            "status":404,
        })
        response.status_code=404
        return response

    @app.route('/app/views/users/<int:user_id>', methods=['DELETE'])
    @token_required
    def delete_user(current_user, user_id):
        if current_user and current_user['isadmin']!=True:
            return make_response(jsonify({
                'status':"failed",
                'message':"you must be an admin"
            }),401)
        if current_user and current_user['isadmin']==True:
            single_user=User()
            userlist= single_user.get_all_User()
            for user in userlist:
                if user['user_id']==user_id:
                    single_user.delete_user(user_id) 

                    response=jsonify({
                        "message":"user deleted successfully",
                        'status':200
                    })
                    response.status_code=200
                    return response
    '''@app.route('/app/views/users/<user_id>', methods=['GET'])
    @token_required
    def activate_cust(current_user, user_id):
        if current_user and current_user['isadmin']!=True:
            return make_response(jsonify({
                'status':"failed",
                'message':"you must be an admin"
            }),401)
        
        if current_user and current_user['isadmin']==True:'''

    @app.route('/app/views/accounts/', methods=['POST'])
    def create_account():
        data = request.get_json()
        
        try:
            user_id=int(data['user_id'])
        
        except Exception:
            response=jsonify({
                "message":"user ID missing",
                "status":400,
            })
            response.status_code=400
            return response 
        user_object= User()
        UserList=user_object.get_all_User()
        account_obj= Account()
        accountlist=account_obj.get_all_accounts()
        for user in UserList:
            if user['user_id'] == user_id:
                account =[
                    account for account in accountlist if account['user_id'] == user_id]
                if account:
                    response = jsonify({
                        "message": "account already exists",
                        "status": 403,
                                })
                    response.status_code = 403
                    return response
                new_account = Account(data)
                new_account.save()
                accountlist = account_obj.get_all_accounts()
                for account in accountlist:
                    if account['user_id'] == user_id:
                        response = jsonify({
                            "message": "Account created successfully",
                            "status": 201,
                            "data": account
                                    })
                        response.status_code = 201
                        return response
        response = jsonify({
                        "message": "User not found",
                        "status": 404,})
        response.status_code=404
        return response
    
    @app.route('/app/views/accounts/<int:account_id>', methods=['DELETE'])
    def delete_account(account_id):
        '''if current_user and current_user['isadmin'] !=True:
            return make_response(
                jsonify({
                    'status':'Failed',
                    'Message':"you must be an admin"

                }), 401)
        if current_user and current_user['isadmin']==True:'''
        single_account= Account()
        accountlist=single_account.get_all_accounts()
        for account in accountlist:
            if account['acc_id']== account_id:
                single_account.delete_account(account_id)

                response=jsonify({
                            'message':'account deleted succesfully',
                            'status':200,
                        })
                response.status_code=200
                return response
        response= jsonify({
                    "message":"account not found",
                    "status":404,
                })
        response.status_code=404
        return response
    
    @app.route('/app/views/accounts/<int:account_id>', methods=['GET'])
    def view_account(account_id):
        single_account=Account()
        accountlist=single_account.get_all_accounts()

        for account in accountlist:
            if account['acc_id']==account_id:
                response=jsonify({
                    "status":200,
                    "data": account
                })
                response.status_code=200
                return response
        response=jsonify({
            'message':'account not found',
            'status':404,
        })
        response.status_code=404
        return response
                











        
    return app