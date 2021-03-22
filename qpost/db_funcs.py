from config import CONNECTION_CONFIG
import mysql.connector
from mysql.connector import errorcode
from .questions import Question
import hashlib
import copy
import os


def select_query(query_string, *q_vars):
    """Helper function for SELECT statements.

    Takes query string and tuple q_vars for  values in query
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
    """Helper function for INSERT, UPDATE or DELETE queries.

    Handles connection and commits queries.
    """
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
    """Hashing function for passwords.

    If salt is not provided, generate a new salt and create a new hash.(creating users)
    Otherwise, generate the hash with the given salt and password.(verifying users)
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
    """Verification for logging in a user.

    Get password hash and salt from database. Hash the given password with the salt and compare with the password has from the database.
    On invalid logins, return None for no user or ['invalid',None] for wrong password or user
    On valid login, return list ['valid', userID ]
    """

    q = "SELECT password_hash, salt, UserID ,is_teacher FROM Users WHERE Users.username = (%s) "

    query_result = select_query(q, (user))
    print(query_result)
    password_hash, salt, UserID, is_teacher = query_result[0]
    new_hash = create_hash(password, salt)
    if new_hash['hash'] == password_hash:
        return ['valid', UserID, is_teacher]
    else:
        return ['invalid', None]


def create_user(username, password):
    """Insert username and hashed password into database."""

    result = create_hash(password)
    modify_query('INSERT INTO Users (username,password_hash,salt) VALUES ((%s), (%s), (%s))',
                 username, result['hash'], result['salt'])

    return verify_login(username, password)


def get_questions(user_id=None):
    """" Get all questions for given user.

    If no user is provided,get all questions.
    Get questions and create a dictionary object {'q_id': Question(question,q_id,user_id))}
    Join answer table with question on the question ID to identify which answers are for the questions the user asked then get all the answers.
    Using the q_id  add the answers to the Question object. then return the list of Question objects
    """

    if user_id:
        questions = select_query(
            "SELECT q_id,question,user_id FROM question WHERE question.user_id = (%s) ORDER BY create_time DESC ", user_id)

        answers = select_query(
            "SELECT answer.q_id, answer.answer, answer.a_id,answer.is_answer FROM answer Left JOIN  question on answer.q_id=question.q_id WHERE question.user_id =(%s)", user_id)
    else:
        questions = select_query(
            "SELECT q_id,question, user_id FROM question")
        answers = select_query(
            "SELECT answer.q_id, answer.answer, answer.a_id, answer.is_answer FROM answer Left JOIN  question on answer.q_id=question.q_id")

    questions = {q_id: copy.deepcopy(
        Question(question, q_id=q_id, user_id=user_id)) for q_id, question, user_id in questions}

    for q_id, answer, a_id, is_answer in answers:
        questions[q_id]['answers'].append((answer, a_id, is_answer))
    return questions.values()


def new_question(question, userID):
    """Insert new question"""

    query_string = "INSERT INTO Question(question,user_id) VALUES (%s,%s)"
    modify_query(query_string, question, userID)
    return True


def answer_question(q_id, answer, u_id):
    """Add an answer for a question."""

    query_string = "INSERT INTO Answer(q_id, answer,user_id) VALUES (%s, %s, %s)"
    modify_query(query_string, q_id, answer, u_id)
    return True


def delete_question(q_id):
    """Delete a question."""

    query_string = "DELETE FROM question WHERE q_id = (%s)"
    modify_query(query_string, q_id)


def delete_answer(a_id):
    """Delete an answer"""

    query_string = "DELETE FROM answer WHERE a_id = (%s)"
    print("DSADSADASDASE", a_id)
    modify_query(query_string, a_id)


def mark_answer(a_id, val):
    """Mark an answer as a selected answer."""

    query_string = "UPDATE answer SET is_answer = (%s)WHERE a_id = (%s)"
    modify_query(query_string, val, a_id)
