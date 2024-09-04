#!/usr/bin/env python3
"""
implementing session authentication system
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    system that uses session authentication mechanisms
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a `user_id`
        """
        if not user_id or not type(user_id) is str:
            return
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
