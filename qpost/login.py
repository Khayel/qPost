from config import CONNECTION_CONFIG
import mysql.connector
from mysql.connector import errorcode
from .questions import Question
import hashlib
import copy
import time
import os


def select_query(query_string, *q_vars):
    """
    helper function for easier SELECT statements
    takes query string and tuple q_vars for  values in query

    """

    try:
        cnx = mysql.connector.connect(**CONNECTION_CONFIG)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        cursor.execute(query_string, q_vars)
        results = cursor.fetchall()
        cnx.close()
        return results


def modify_query(query_string, *q_vars):
    try:
        cnx = mysql.connector.connect(**CONNECTION_CONFIG)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with connection username and password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        cursor.execute(query_string, q_vars)
        cnx.commit()
        cnx.close()
        return True


def create_hash(password, salt=None):
    """
    Hashing function
    if salt is not provided, create a new user with new hash
    otherwise take hex into salt and return dict with hash, and salt
    returns {'hash': hash in hex, 'salt': salt in hex}

    """
    if not salt:
        salt = os.urandom(8)
    else:
        salt = bytes.fromhex(salt)

    return {'hash': hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    ).hex(), 'salt': salt.hex()}


def verify_login(user, password):
    """
    Verification for logging in a user.
    Based on username get password hash and salt from database. Hash given password with the salt retrieved and cooompare with database.
    On invalid logins, return 'no_user' or 'invalid'
    On valid login, return list ['valid', userID ]
    """
    q = f"SELECT password_hash, salt, UserID FROM Users WHERE Users.username = (%s) "
    result = select_query(q, (user))
    if not result:
        return 'no_user'
    new_hash = create_hash(password, result[0][1])
    print(new_hash)
    if new_hash['hash'] == result[0][0]:
        return ['valid', result[0][2]]
    else:
        return 'invalid'


def create_user(username, password):
    """
    TODO FIX
    return s user id
    """
    result = create_hash(password)
    modify_query('INSERT INTO Users (username,password_hash,salt) VALUES ((%s), (%s), (%s))',
                 username, result['hash'], result['salt'])

    return verify_login(username, password)


def get_my_questions(user_id):
    """"
    Returns a list of Question objects
    TODO change to user_id
    questions - gets all questions of username
    answers - get all answers for all the questions asked by the user

    """
    questions = select_query(
        "SELECT q_id,question FROM question WHERE question.user_id = (%s) ORDER BY create_time DESC ", user_id)

    answers = select_query(
        "SELECT answer.q_id, answer.answer, answer.a_id,answer.is_answer FROM answer Left JOIN  question on answer.q_id=question.q_id WHERE question.user_id =(%s)", user_id)
    my_questions = {q[0]: copy.deepcopy(
        Question(q[1], q_id=q[0], user_id=user_id)) for q in questions}

    for a in answers:
        my_questions[a[0]]['answers'].append((a[1], a[2], a[3]))
    print(my_questions.values())
    return my_questions.values()


def get_all_questions(user_id):
    """"
    returns a list of Question objects.

    """
    questions = select_query(
        "SELECT q_id,question, user_id FROM question")
    my_questions = {q[0]: copy.deepcopy(
        Question(q[1], q_id=q[0], user_id=q[2])) for q in questions}

    answers = select_query(
        "SELECT answer.q_id, answer.answer, answer.a_id, answer.is_answer FROM answer Left JOIN  question on answer.q_id=question.q_id")
    for a in answers:
        my_questions[a[0]]['answers'].append((a[1], a[2], a[3]))
    return my_questions.values()


def new_question(question, userID):
    """
    Insert new question
    """
    query_string = "INSERT INTO Question(question,user_id) VALUES (%s,%s)"
    modify_query(query_string, question, userID)
    return True


def answer_question(q_id, answer, u_id):
    query_string = "INSERT INTO Answer(q_id, answer,user_id) VALUES (%s, %s, %s)"
    modify_query(query_string, q_id, answer, u_id)
    return True


def delete_question(q_id):
    query_string = "DELETE FROM question WHERE q_id = (%s)"
    modify_query(query_string, q_id)


def make_answer(a_id):
    query_string = "UPDATE answer SET is_answer = TRUE WHERE a_id = (%s)"
    modify_query(query_string, a_id)
