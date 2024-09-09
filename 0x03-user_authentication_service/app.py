#!/usr/bin/env python3
"""
set up a basic Flask app
"""
from flask import Flask, json, jsonify, request
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
