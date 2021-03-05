
import mysql.connector
from mysql.connector import errorcode
import hashlib
import os


def select_query(query_string):
    connction_config = {
        'user': 'root',
        'password': 'T3mp3r3d1!',
        'host': '127.0.0.1',
        'database': 'globalchat',
        'raise_on_warnings': True
    }


def create_hash(password, salt=None):
    # if salt not provided assume creating a new user
    # if salt provided assume verifying user
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
    connction_config = {
        'user': 'root',
        'password': 'T3mp3r3d1!',
        'host': '127.0.0.1',
        'database': 'globalchat',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**connction_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        q = f"SELECT password_hash, salt FROM User WHERE User.username = '{user}' "
        cursor = cnx.cursor()

        cursor.execute(q)
        result = cursor.fetchone()
        if not result:
            return 'no_user'
        print(result)
        new_hash = create_hash(password, result[1])
        print(new_hash)
        if new_hash['hash'] == result[0]:
            return 'valid'
        else:
            return 'invalid'


def create_user(username, password):
    result = create_hash(password)
    connction_config = {
        'user': 'root',
        'password': 'T3mp3r3d1!',
        'host': '127.0.0.1',
        'database': 'globalchat',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**connction_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:

        cursor = cnx.cursor()
        query = 'INSERT INTO User (username,password_hash,salt) VALUES ("{}", "{}", "{}")'.format(
            username, result['hash'], result['salt'])
        print(query)
        cursor.execute(query)
        cnx.commit()
        cnx.close()


if __name__ == "__main__":
    print("FDSFDS")
    # create_user(input("Username: "), input("Passwrd: "))
    if verify_login(input("user: "), input("pass: ")):
        print("SUCCESS")
    else:
        print(" FAIL")
