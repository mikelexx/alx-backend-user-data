#!/usr/bin/env python3
"""
Flask view to handle all routes for the Session authentication
"""
from api.v1.views import app_views
from flask import abort, app, current_app, jsonify, request
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def autheticate_session():
    """
    authenticated requests and sets a cookie to enable
    session authenication for next request using cookies
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    if not user_email:
        return jsonify({'error': 'email missing'}), 400
    if not user_pwd:
        return jsonify({'error': 'password missing'}), 400
    try:
        users = User.search({'email': user_email})
        if not users:
            return jsonify({'error': 'no user found for this email'}), 404
        for user in users:
            if user and user.is_valid_password(user_pwd):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                resp = jsonify(user.to_json())
                cookie_name = os.getenv('SESSION_NAME')
                resp.set_cookie(cookie_name, session_id)
                return resp
        return jsonify({'error': 'wrong password'}), 401
    except Exception as e:
        return jsonify({'error': 'no user found for this email'}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def log_out_of_session():
    """
    deletes session associated from this request
    (logout the user of this session)
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
