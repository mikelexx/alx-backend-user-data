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
        TODO
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        TODO
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        TODO
        """
        return None
