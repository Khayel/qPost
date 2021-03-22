from flask import render_template, url_for, request, session, redirect, jsonify
from flask.blueprints import Blueprint
from .db_funcs import *
from .decorators import login_required
from http import HTTPStatus

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def index():
    """ Default page showing logged in user's question."""

    return render_template('index.html',
                           username=session['username'],
                           user_id=session['user_id'],
                           is_mine=True,
                           my_questions=get_questions(session['user_id']))


@ views.route('/login', methods=['POST', 'GET'])
def login():
    """Login page

    Log in the user and add session variables. A POST request is action login.
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # check if form is sign_in or create_user
        if request.form.get('sign_in'):
            login_status = verify_login(request.form.get('username'),
                                        request.form.get('password'))
            if not login_status:
                return render_template('login.html', status="no_user")
            elif login_status[0] == "valid":
                session['username'] = request.form.get('username')
                session['user_id'] = login_status[1]
                return redirect(url_for('views.index'))
            elif login_status[0] == "invalid":
                return render_template('login.html', status="invalid")
        else:
            new_user = create_user(request.form.get('username'),
                                   request.form.get('password'))
            session['username'] = request.form.get('username')
            session['user_id'] = new_user[1]
            return redirect(url_for('views.index'))


@ views.route('/logout')
def logout():
    """Remove session variables and redirect to login page"""

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('views.login'))


@ views.route('/question', methods=["GET"])
def question():
    """Display all questions and answers."""

    return render_template(
        'index.html',
        username=session['username'],
        user_id=session['user_id'],
        is_mine=False,
        my_questions=get_questions())


@ views.route('/answer/<action>', methods=["POST"])
@ login_required
def answer(action):
    """POST operations for an answer.
    add, delete, select, and deselect an answer 
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
    """POST operations for a question.
    create and delete questions.
    """

    if action == "delete":
        delete_question(request.form.get('q_id'))
    elif action == "new":
        new_question(request.form.get('question'), session['user_id'])
    else:
        return HTTPStatus.BAD_REQUEST

    return redirect(request.referrer)
