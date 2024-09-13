#!/usr/bin/env python3
"""
set up a basic Flask app
"""

from flask import Flask, jsonify, redirect, request, abort
from flask import url_for
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    creates a new session for the user, stores it's session ID
    as cookie with key "session_id" on the response
    retuns:json code and status code 200 for sucess, else aborts
    with 401 status code
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    basic route setup
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    an  api point to register user
    must supply : email, password
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': f'{email}', 'message': 'user created'})
    except Exception:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    finds the user with given session id from cookie and destroys it,
    then redirects to `GET /`. If the user doesn't
    exist, aborts with 403 status
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    gets a user profile using session id from cookie
    """
    session_id = request.cookies.get('session_id')
    if not session_id or not type(session_id) is str:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    generates a token
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    updates user password
    required:
            'email', 'reset_token'
    """
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    email = request.form.get('email')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'})
    except Exception:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
