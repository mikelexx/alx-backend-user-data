#!/usr/bin/env python3
"""
Authentication system using database stored Sessions
"""
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    parsistent sessions authentication class for sessions
    """

    def create_session(self, user_id=None) -> str:
        """
        creates and stores new instance of UserSession and returns
        the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return
        user_session_id = UserSession(user_id=user_id, session_id=session_id)
        user_session_id.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        returns `user_id` by requesting UserSession in the
        database based on `session_id`
        """
        user_session = UserSession.get(session_id)
        if user_session:
            return user_session.get('user_id')

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID
        from the `request` cookie
        """
        session_id = self.session_cookie(request)
        user_session = UserSession.get(session_id)
        user_session.remove()
