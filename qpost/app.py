from flask import Flask, render_template, url_for, request, session
from flask_restful import Resource, Api
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


app = Flask(__name__)
api = Api(app)
api.add_resource(loginAction, '/api/login')
api.add_resource(userAction, '/api/user')


@app.route('/')
def index():
    if session['username']:
        return render_template('index.html',)

    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        login_status = verify_login(request.form.get('username'),
                                    request.form.get('password'))
        if login_status:

            print("Login successful")
            # redirect  with flask login
        else:
            print("PLEASE TRY AGAIN")
            print("wrong password")
            # prompt wrong password

        return"DSAD"
