from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.helpers.helpers_authorization import verify_administrator
from app.helpers.helpers_user_management import create_users, update_users, delete_users

app = Blueprint("admin_user_management", __name__, url_prefix="")


@app.route("/api/admin/users", methods=['POST'])
@jwt_required
def admin_create_user():
    """
            Endpoint for user creation

            Requires JWT authorization and user to be ADMIN

            *Accepts BOTH array and object as parameters (for single or multiple user creation). Given example is object.*
            ---
            parameters:
              - name:
                in: body
                required: true
                type: array
                schema:
                    id:
                    name:
                    type: array
                    properties:
                        username:
                            type: string
                            example: cosminPopa97
                        password:
                            type: string
                            example: some string in base64
                        first_name:
                            type: string
                            example: Cosmin
                        last_name:
                            type: string
                            example: Popa
                        valid_account:
                            type: bool
                            example: 0
                        is_phd:
                            type: bool
                            example: 1
                        educational_title:
                            type: string
                            example: Profesor Doctor Inginer
            responses:
              200:
                description: Validates that user was created successfully.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Users created successfully.
              400:
                description: Returns if request is invalid
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Invalid fields for users.
              403:
                description: Returns if user does not have role ADMINISTRATOR
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Invalid role for request
              500:
                description: Returns if something goes wrong with the sql query
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Something went wrong while creating users.
    """
    verify_administrator(get_jwt_identity())
    users = request.json
    response, status_code = create_users(users)
    return jsonify({"msg": response}), status_code


@app.route("/api/admin/users", methods=['PUT'])
@jwt_required
def admin_update_user():
    """
            Endpoint for user updates, using username as id (username will not be changed.)

            Requires JWT authorization and user to be ADMIN

            *Accepts BOTH array and object as parameters (for single or multiple user creation). Given example is object.*
            ---
            parameters:
              - name:
                in: body
                required: true
                type: array
                schema:
                    id:
                    name:
                    type: array
                    properties:
                        username:
                            type: string
                            example: cosminPopa97
                        first_name:
                            type: string
                            example: Cosmin
                        last_name:
                            type: string
                            example: Popa
                        valid_account:
                            type: bool
                            example: 0
                        is_phd:
                            type: bool
                            example: 1
                        educational_title:
                            type: string
                            example: Profesor Doctor Inginer
            responses:
              200:
                description: Validates that user was updated successfully.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Users created successfully.
              204:
                description: Returns if no update has been applied.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Users have not been modified.
              403:
                description: Returns if user does not have role ADMINISTRATOR
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Invalid role for request
              500:
                description: Returns if something goes wrong with the sql query
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Something went wrong while updating users.
    """
    verify_administrator(get_jwt_identity())
    users = request.json
    response, status_code = update_users(users)
    return jsonify({"msg": response}), status_code


@app.route("/api/admin/users", methods=['DELETE'])
@jwt_required
def admin_delete_user():
    """
            Endpoint for user deletion, using username as id

            Requires JWT authorization and user to be ADMIN

            *Accepts BOTH array and object as parameters (for single or multiple user creation). Given example is object.*
            ---
            parameters:
              - name:
                in: body
                required: true
                type: array
                schema:
                    id:
                    name:
                    type: array
                    properties:
                        username:
                            type: string
                            example: cosminPopa97
            responses:
              200:
                description: Validates that user was deleted successfully.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Users deleted successfully.
              404:
                description: Returns if no user with given username has been found.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Users have not been modified.
              403:
                description: Returns if user does not have role ADMINISTRATOR
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Invalid role for request
              500:
                description: Returns if something goes wrong with the sql query
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Something went wrong while deleting users.
    """
    verify_administrator(get_jwt_identity())
    users = request.json
    response, status_code = delete_users(users)
    return jsonify({"msg": response}), status_code
