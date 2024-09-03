#!/usr/bin/env python3
"""
implements Basic authenticate scheme
"""
import base64
from .auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    this will authenticate requests using Basic Auth scheme
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        args:
        authorization_header: authorization header
            supposed to contain scheme and credentials part
        returns the Base64 part of the Authorization header for
        a Basic Authentication
        """
        if not authorization_header \
                or type(authorization_header) is not str \
                or not authorization_header.startswith('Basic '):
            return
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Args:
            base64_authorization_header: base64 string
        returns the decoded value
        of a Base64 string base64_authorization_header
        """
        if not base64_authorization_header \
                or type(base64_authorization_header) is not str:
            return
        try:
            base64_decoded_str = base64.b64decode(base64_authorization_header)
            return base64_decoded_str.decode('utf-8')
        except Exception as e:
            return

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        args:
        decode_base64_authorization_header: decoded base64 part of
        authorization_header (one that contains credentials)
        returns the user email and password from the Base64 decoded value.
        """
        if not decoded_base64_authorization_header \
                or type(decoded_base64_authorization_header) is not str \
                or ':' not in decoded_base64_authorization_header:
            return (None, None)

        credentials = decoded_base64_authorization_header.split(':', 1)
        if len(credentials) > 2:
            return (credentials[0], "".join(credentials[1::]))
        return tuple(credentials)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns `User` instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return
        if user_pwd is None or type(user_pwd) is not str:
            return
        users = User.search({'email': user_email})
        for user in users:
            if user and user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
         performs basic Authentication for the request user
         """
        auth_header = self.authorization_header(request)
        if auth_header:
            base64_credentials = self.extract_base64_authorization_header(
                auth_header)
            if base64_credentials:
                base64_decoded_credentials = \
                        self.decode_base64_authorization_header(
                                base64_credentials)
                if base64_decoded_credentials:
                    user_email, password = self.extract_user_credentials(
                        base64_decoded_credentials)
                    if user_email and password:
                        user = self.user_object_from_credentials(
                            user_email, password)
                        return user
