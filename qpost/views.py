from flask import Flask, render_template, url_for, request, session, redirect
from flask.blueprints import Blueprint
from flask_restful import Resource, Api
from .login import answer_question, get_all_questions, new_question, verify_login, get_my_questions
# from .questions import Question
from .decorators import login_required

views = Blueprint('views', __name__)


@views.route('/')
def index():
    """
    Home page
    if signed out redirect to login page
    When signed in, pull my
    """
    if 'username' in session:
        return render_template('index.html', username=session['username'], is_mine=True,
                               my_questions=get_my_questions(
                                   username=session['username']))
    return redirect(url_for('views.login'))


@ views.route('/teacher')
@ login_required
def myPage():
    return "Teacher management page goes here"


@ views.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        login_status = verify_login(request.form.get('username'),
                                    request.form.get('password'))
        if login_status[0] == "valid":
            session['username'] = request.form.get('username')
            session['user_id'] = login_status[1]
            print(session)
            print("Login successful")
            return redirect(url_for('views.index'))
            # redirect  with flask login
        elif login_status == "invalid":
            return render_template('login.html', status="invalid")
        else:
            return render_template('login.html', status="no_user")


@views.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('views.login'))


@views.route('/question', methods=["POST", "GET"])
def question():
    if request.method == "POST":
        print(request.form.get('question'), session['user_id'])
        print(session['user_id'])
        if new_question(request.form.get('question'), session['user_id'],):
            return redirect(url_for('views.index'))
        else:
            return "Error, Please try again."
    else:
        return render_template('index.html', username=session['username'], is_mine=False, my_questions=get_all_questions(session['user_id']))


@views.route('/answer', methods=["POST"])
def answer():
    if answer_question(request.form.get('q_id'), request.form.get('answer_input'), session['user_id']):
        return redirect(url_for('views.index'))
    else:
        return "Error, Please try again."
