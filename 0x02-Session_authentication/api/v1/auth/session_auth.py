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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a session ID `session_id`
        """
        if not session_id or not type(session_id) is str:
            return
        return self.user_id_by_session_id.get(session_id)
