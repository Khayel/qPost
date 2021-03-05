from flask_restful import Resource, Api
from flask import request
from .login import verify_login, create_user, select_query


class loginAction(Resource):
    def post(self):
        status = verify_login(request.form.get('username'),
                              request.form.get('password'))
        if status == 'valid':
            print("Login successful")
            return {
                "status": "success",
            }
            # redirect  with flask login
        elif status == 'invalid':
            print("wrong password")
            # prompt wrong password
        else:
            print("USER doesnt exist")
            # prompt to register


class userAction(Resource):
    def get(self):
        return select_query(f"SELECT * FROM User WHERE User.username='{request.args.get('username')}'")

    def post(self):
        status = create_user(request.form.get('username'),
                             request.form.get('password'))
        if status == 'succes':
            return {
                "status": "success"
            }
        else:
            return {"status": "error"}
