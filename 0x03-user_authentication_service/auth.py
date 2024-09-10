#!/usr/bin/env python3
"""
hashing password
"""

import bcrypt
from typing import Union
from uuid import uuid4
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    returns a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        saves a new user to database, or else it raises ValueError
        if user already exists
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password.decode('utf-8'))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        verifies the use loging in using `email` and `password`
        credentials is recognized/valid
        """
        try:
            user = self._db.find_user_by(email=email)
            is_valid_pwd = bcrypt.checkpw(password.encode('utf-8'),
                                          user.hashed_password.encode('utf-8'))
            return is_valid_pwd
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """
        generates a random uuid, and returns a string reprentation
        of the id
        """
        return uuid4().__str__()

    def create_session(self, email: str) -> str:
        """
        finds user corresponding to the email, generates a new UUID and
        stores it in the database as the user's session ID, then returns
        the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            new_session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=new_session_id)
            return new_session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        gets and returns user from database
        using `session_id` provided else returns None if user not found
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding user's session ID to none
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a UUID and updates the user matching the `email`
        reset_token
        database field
        raises:
            ValueError: if the user doesn't exist
        returns: generated uuid
        """
        try:
            user = self._db.find_user_by(email=email)
            uuid = self._generate_uuid()
            setattr(user, 'reset_token', uuid)
            return uuid
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
            updates the user's password with the new `password` provided
            raises:
                ValueError: if no user matching the `reset_token` is found
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except Exception:
            raise ValueError
