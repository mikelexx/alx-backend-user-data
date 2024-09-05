#!/usr/bin/env python3
"""
Session authentication system with added Session expiry
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    adds session expiry in the SessionAuth system
    """

    def __init__(self):
        super().__init__()
        try:
            session_duration = int(os.getenv('SESSION_DURATION'))
            self.session_duration = session_duration
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
       creates session for `user_id` with and notes its
       time of creation
       returns: session id
       """
        session_id = super().create_session(user_id)
        if not session_id:
            return
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        extracts user_id from the `session_id` provided
        if the session has not expired yet else returns None
        """
        if not session_id or not type(session_id) is str \
                or session_id not in self.user_id_by_session_id:
            return
        session_dictionary = self.user_id_by_session_id.get(session_id)
        user_id = session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if self.session_duration <= 0:
            return user_id
        if not created_at:
            return
        if (datetime.now() - created_at).seconds > self.session_duration:
            return
        return user_id
