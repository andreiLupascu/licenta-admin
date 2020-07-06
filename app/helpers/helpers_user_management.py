import base64

import pymysql
from flask import current_app
from flask_mail import Message, Mail
from passlib.handlers.bcrypt import bcrypt

from app.helpers.helpers_database import get_connection


def create_users(users):
    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        try:
            if not isinstance(users, list):
                users = [users]
            email_list = []
            for user in users:
                username = user['username']
                password = bcrypt.encrypt(base64.b64decode(user['password']).decode("utf-8"))
                first_name = user['first_name']
                last_name = user['last_name']
                valid_account = user['valid_account']
                is_phd = user['is_phd']
                educational_title = user['educational_title']
                cur.execute(
                    'INSERT INTO user(username, password, first_name, last_name, valid_account, is_phd,'
                    ' educational_title) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (username, password, first_name, last_name, valid_account, is_phd, educational_title,))
                email_list.append(username)
            conn.commit()
            conn.close()
            mail = Mail(current_app)
            msg = Message(subject='Account created.', sender=current_app.config['MAIL_USERNAME'], recipients=email_list)
            msg.body = "Your account has been created, download the conference application to activate your account!"
            mail.send(msg)
            return f'Users created successfully.', 200
        except Exception as e:
            print(e)
            conn.close()
            if 'Duplicate' in e.args[1]:
                return f'Username already exists.', 400
            return f'Something went wrong while creating users.', 500


def update_users(users):
    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        try:
            if not isinstance(users, list):
                users = [users]
            affected_rows = [0] * len(users)
            for user in users:
                username = user['username']
                first_name = user['first_name']
                last_name = user['last_name']
                valid_account = user['valid_account']
                is_phd = user['is_phd']
                educational_title = user['educational_title']
                affected_rows[users.index(user)] = cur.execute('UPDATE user '
                                                               'set '
                                                               'first_name=%s,'
                                                               'last_name=%s,'
                                                               'valid_account=%s,'
                                                               'is_phd=%s,'
                                                               'educational_title=%s '
                                                               'WHERE username=%s;',
                                                               (first_name, last_name, valid_account, is_phd,
                                                                educational_title, username,))
            if 0 not in affected_rows:
                conn.commit()
                conn.close()
                return f'Users updated successfully.', 200
            else:
                conn.close()
                return f'Users either do not exist or have not been modified.', 204
        except Exception as e:
            print(e)
            conn.close()
            return f'Something went wrong while updating users.', 500


def delete_users(users):
    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        try:
            if not isinstance(users, list):
                users = [users]
            affected_rows = [0] * len(users)
            for user in users:
                username = user['username']
                affected_rows[users.index(user)] = cur.execute('DELETE FROM user WHERE username=%s;', (username,))
            if 0 not in affected_rows:
                conn.commit()
                conn.close()
                return f'Users deleted successfully.', 200
            else:
                conn.close()
                return f'Given users do not exist.', 404
        except Exception as e:
            print(e)
            conn.close()
            return f'Something went wrong while deleting users.', 500
