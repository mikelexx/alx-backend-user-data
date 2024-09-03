#!/usr/bin/env python3
"""
authentication system
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    for managing API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if the request path is excluded
        """
        if path is None or not excluded_paths:
            return True
        excluded_paths = [ 
                          path[::-1] if path[-1] == '*' else path for path in excluded_paths
        ]
        if path in excluded_paths or path + '/' in excluded_paths:
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
