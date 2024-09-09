#!/usr/bin/env python3
"""
set up a basic Flask app
"""
from flask import Flask, json, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    basic route setup
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """
    an  api point to register user
    must supply : email, password
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify({'email': f'{email}', 'message': 'user created'})
    except Exception:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    logs in an user and registers a new session id for the user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid_user = auth.valid_login(email, password)
    if not is_valid_user:
        abort(401)
    session_id = auth.create_session(email)
    resp = jsonify({'email': email, 'message': 'logged in'})
    resp.set_cookie('session_id', session_id)
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
