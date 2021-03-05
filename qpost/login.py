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
    function for easier SELECT statements
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
    q = f"SELECT password_hash, salt,UserID FROM Users WHERE Users.username = (%s) "
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
    result = create_hash(password)
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
        query = 'INSERT INTO Users (username,password_hash,salt) VALUES ((%s), (%s), (%s))'
        cursor.execute(query, (username, result['hash'], result['salt'], time.strftime(
            '%Y-%m-%d %H:%M:%S')))
        cnx.commit()
        cnx.close()
        return


def get_my_questions(username):
    """"
    returns a list of Question objects.


    """
    print("HERE")
    # result = select_query("SELECT answer.answer,question.question, answer.a_id,  answer.q_id  FROM answer Left JOIN  question on answer.q_id=question.q_id WHERE question.user_id in (SELECT userid from users WHERE username=(%s))", username)
    my_questions = {}
    questions = select_query(
        "SELECT q_id,question FROM question WHERE question.user_id in (SELECT userid from users WHERE username=(%s)) ORDER BY create_time DESC ", username)
    my_questions = {q[0]: copy.deepcopy(
        Question(q[1], q_id=q[0])) for q in questions}
    answers = select_query(
        "SELECT answer.q_id, answer.answer  FROM answer Left JOIN  question on answer.q_id=question.q_id WHERE question.user_id in (SELECT userid from users WHERE username=(%s))", username)
    for a in answers:
        print(a)
        if a[0] in my_questions.keys():
            my_questions[a[0]]['answers'].append(a[1])

            # shallow copy fix....
            # if len(my_questions[a[0]]['answers']) == 0:
            #     my_questions[a[0]]['answers'] = [a[1]]
            # else:
            #     my_questions[a[0]]['answers'] = [
            #         *my_questions[a[0]]['answers'], a[1]]

        else:
            print("should never happen check")
    print(my_questions.values())
    return my_questions.values()


def get_all_questions(user_id):
    """"
    returns a list of Question objects.


    """
    print("HERE")
    # result = select_query("SELECT answer.answer,question.question, answer.a_id,  answer.q_id  FROM answer Left JOIN  question on answer.q_id=question.q_id WHERE question.user_id in (SELECT userid from users WHERE username=(%s))", username)
    my_questions = {}
    questions = select_query(
        "SELECT q_id,question FROM question")
    my_questions = {q[0]: copy.deepcopy(
        Question(q[1], q_id=q[0])) for q in questions}
    answers = select_query(
        "SELECT answer.q_id, answer.answer  FROM answer Left JOIN  question on answer.q_id=question.q_id")
    for a in answers:
        print(a)
        if a[0] in my_questions.keys():
            my_questions[a[0]]['answers'].append(a[1])

            # shallow copy fix....
            # if len(my_questions[a[0]]['answers']) == 0:
            #     my_questions[a[0]]['answers'] = [a[1]]
            # else:
            #     my_questions[a[0]]['answers'] = [
            #         *my_questions[a[0]]['answers'], a[1]]

        else:
            print("should never happen check")
    print(my_questions.values())
    return my_questions.values()


def new_question(question, userID):
    """
    Insert new question
    """
    query_string = "INSERT INTO Question(question,user_id) VALUES (%s,%s)"
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
        cursor.execute(query_string, (question, userID))
        cnx.commit()
        cnx.close()
        return True


def answer_question(q_id, answer, u_id):
    query_string = "INSERT INTO Answer(q_id, answer,user_id) VALUES (%s, %s, %s)"
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
        cursor.execute(query_string, (q_id, answer, u_id))
        cnx.commit()
        cnx.close()
        return True


def delete_question(q_id):
    query_string = "INSERT INTO Answer(q_id, answer,user_id) VALUES (%s, %s, %s)"
    pass
