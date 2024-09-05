#!/usr/bin/env python3
"""
authentication system based on Session ID stored in
database to avoid losing all Session IDs one the
application stops
"""
from models.base import Base


class UserSession(Base):
    """
    model(template) for creating persisintent user_id and session_id
    on the database
    """
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
