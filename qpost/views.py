from flask import render_template, url_for, request, session, redirect, jsonify
from flask.blueprints import Blueprint
from .login import *
from .decorators import login_required
from http import HTTPStatus
views = Blueprint('views', __name__)


@views.route('/')
@login_required
def index():
    """
    Default Home Page
    View the current user's questions.
    """
    return render_template('index.html',
                           username=session['username'],
                           user_id=session['user_id'],
                           is_mine=True,
                           my_questions=get_my_questions(session['user_id']))


@ views.route('/teacher')
@ login_required
def myPage():
    return "Teacher management page goes here"


@ views.route('/login', methods=['POST', 'GET'])
def login():
    """
    Login page
    Log in the user and add session variables
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('sign_in'):
            login_status = verify_login(request.form.get('username'),
                                        request.form.get('password'))
            if login_status[0] == "valid":
                session['username'] = request.form.get('username')
                session['user_id'] = login_status[1]
                print(session)
                print("Login successful")
                return redirect(url_for('views.index'))
            elif login_status == "invalid":
                return render_template('login.html', status="invalid")
            else:
                return render_template('login.html', status="no_user")
        else:
            new_user = create_user(request.form.get('username'),
                                   request.form.get('password'))
            session['username'] = request.form.get('username')
            session['user_id'] = new_user[1]
            return redirect(url_for('views.index'))


@ views.route('/logout')
def logout():
    """
    Remove session variables and logout user
    """
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('views.login'))


@ views.route('/question', methods=["POST", "GET"])
def question():
    """
    Display all questions and answers.
    """
    return render_template(
        'index.html',
        username=session['username'],
        user_id=session['user_id'],
        is_mine=False,
        my_questions=get_all_questions(session['user_id']))


@ views.route('/answer/<action>', methods=["POST"])
@ login_required
def answer(action):
    """
    Answer a question assuming user is logged in
    """
    if action == "add":
        answer_question(request.form.get('q_id'), request.form.get(
            'answer_input'), session['user_id'])
    elif action == "delete":
        delete_answer(request.form.get('a_id'))
        return redirect(request.referrer)
    elif action == "selected":
        mark_answer(request.form.get('a_id'), 1)
    elif action == "unselected":
        mark_answer(request.form.get('a_id'), 0)
    else:
        return HTTPStatus.BAD_REQUEST

    return redirect(request.referrer)


@ views.route('/question/<action>', methods=['POST'])
@ login_required
def question_action(action):
    if action == "delete":
        delete_question(request.form.get('q_id'))
    elif action == "new":
        new_question(request.form.get('question'), session['user_id'])
    else:
        return HTTPStatus.BAD_REQUEST

    return redirect(request.referrer)
