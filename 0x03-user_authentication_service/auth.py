#!/usr/bin/env python3
"""
hashing password
"""
import bcrypt
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
        except Exception as e:
            return False
