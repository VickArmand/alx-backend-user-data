#!/usr/bin/env python3
"""app module starts the flask app
and contains routes"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """end-point to register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """function to respond to the POST /sessions route"""
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid = AUTH.valid_login(email, password)
    if not is_valid:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": "{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ respond to the DELETE /sessions route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    respond to the GET /profile route.
    The request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist,
    respond with a 200 HTTP status and the following JSON payload:
    {"email": "<user email>"}
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    respond to the PUT /reset_password route.
    The request is expected to contain form data with fields
    "email", "reset_token" and "new_password".
    Update the password.
    If the token is invalid, catch the exception
    and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 HTTP code
    and the following JSON payload:
    {"email": "<user email>", "message": "Password updated"}
    """
    email = request.form.get("email")
    token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(token, new_password)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    respond to the POST /reset_password route.
    The request is expected to contain form data with the "email" field.
    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status
    and the following JSON payload:
    {"email": "<user email>", "reset_token": "<reset token>"}
    """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
