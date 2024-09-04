#!/usr/bin/env python3
"""
authentication system
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    for managing API authentication
    """
    _my_session_id = os.getenv('SESSION_NAME')

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if the request path is excluded
        """
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path[:-1]) \
                    and excluded_path[-1] == '*' \
                    or excluded_path == path or excluded_path == path + '/':
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        checks for authorization_header in request and returns one
        if found
        """
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        TODO -> GET CURRENT USER OF THE REQUEST FROM DATABASE
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value(session id) from a request
        """
        if not request:
            return
        session_id = request.cookies.get(self._my_session_id)
        return session_id
