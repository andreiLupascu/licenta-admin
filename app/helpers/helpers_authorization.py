from flask import jsonify


def verify_administrator(current_user):
    if 'ADMINISTRATOR' not in current_user['roles']:
        return jsonify({"msg": "Invalid role for request"}), 403


def verify_program_committee(current_user):
    if 'PROGRAM_COMMITTEE' not in current_user['roles'] and 'ADMINISTRATOR' not in current_user['roles']:
        return jsonify({"msg": "Invalid role for request"}), 403
