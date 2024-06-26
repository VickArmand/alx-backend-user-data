#!/usr/bin/env python3
""" session_auth module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login():
    """create a route POST /auth_session/login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    is_valid = users[0].is_valid_password(password)
    if not is_valid:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    cookie_name = os.getenv('SESSION_NAME')
    response = jsonify(users[0].to_json())
    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['POST'],
                 strict_slashes=False)
def logout():
    """adding a new route DELETE /api/v1/auth_session/logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
