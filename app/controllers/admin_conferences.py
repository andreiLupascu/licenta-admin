from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.helpers.helpers_conferences import create_conference, update_conference, delete_conference
from app.helpers.helpers_authorization import verify_administrator

app = Blueprint("admin_conferences", __name__, url_prefix="")


@app.route("/api/admin/conferences", methods=['POST'])
@jwt_required
def admin_create_conferences():
    """
            Endpoint for conference creation
            requires JWT authorization and user to be ADMIN
            ---
            parameters:
              - name:
                in: body
                required: true
                schema:
                    id:
                    properties:
                        title:
                            type: string
                            example: Conferinta
                        location:
                            type: string
                            example: Romania
                        country:
                            type: string
                            example: Tot Romania
                        start_date:
                            type: timestamp
                            example: 1584437524
                        end_date:
                            type: timestamp
                            example: 1584437525
            responses:
              200:
                description: Validates that conference {title} was created successfully.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Conference Conferinta created successfully.
              400:
                description: Returns if request is invalid
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Something went wrong while creating conference Conferinta.
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
                            example: Something went wrong while creating conference Conferinta.
        """
    verify_administrator(get_jwt_identity())
    conference = request.json
    response, status_code = create_conference(conference)
    return jsonify({"msg": response}), status_code


@app.route("/api/admin/conferences", methods=['PUT'])
@jwt_required
def admin_update_conferences():
    """
                Endpoint for conference updates
                requires JWT authorization and user to be ADMIN
                ---
                parameters:
                  - name:
                    in: body
                    required: true
                    schema:
                        id:
                        properties:
                            title:
                                type: string
                                example: Conferinta
                            location:
                                type: string
                                example: Romania
                            country:
                                type: string
                                example: Tot Romania
                            start_date:
                                type: timestamp
                                example: 1584437524
                            end_date:
                                type: timestamp
                                example: 1584437525
                            path_to_logo:
                                type: string
                                example: link_catre_fisier.png
                            path_to_description:
                                type: string
                                example: link_catre_descriere.pdf
                responses:
                  200:
                    description: Validates that conference {title} was updated successfully.
                    schema:
                        id:
                        properties:
                            msg:
                                type: string
                                example: Conference Conferinta updated successfully.
                  204:
                    description: If target conference title does not exist OR if no updates can be done from the request
                  400:
                    description: Returns if request is invalid/ if trying to update non-existing fields
                    schema:
                        id:
                        properties:
                            msg:
                                type: string
                                example: Request contains invalid fields for conference.
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
                                example: Something went wrong while updating conference Conferinta.
            """
    verify_administrator(get_jwt_identity())
    conference = request.json
    response, status_code = update_conference(conference)
    return jsonify({"msg": response}), status_code


@app.route("/api/admin/conferences", methods=['DELETE'])
@jwt_required
def admin_delete_conferences():
    """
            Endpoint for conference deletion
            requires JWT authorization and user to be ADMIN
            ---
            parameters:
              - name:
                in: body
                required: true
                schema:
                    id:
                    properties:
                        title:
                            type: string
                            example: Conferinta
            responses:
              200:
                description: Validates that conference {title} was deleted successfully.
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Conference Conferinta deleted successfully.
              403:
                description: Returns if user does not have role ADMINISTRATOR
                schema:
                    id:
                    properties:
                    msg:
                            type: string
                            example: Invalid role for request
              404:
                description: Returns if given title is not found
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Conference Conferinta does not exist.
              500:
                description: Returns if something goes wrong with the sql query
                schema:
                    id:
                    properties:
                        msg:
                            type: string
                            example: Something went wrong while creating conference Conferinta.
        """
    verify_administrator(get_jwt_identity())
    conference = request.json
    response, status_code = delete_conference(conference)
    return jsonify({"msg": response}), status_code
