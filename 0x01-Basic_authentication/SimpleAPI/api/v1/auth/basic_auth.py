#!/usr/bin/env python3
"""
implements Basic authenticate scheme
"""
import base64
from .auth import Auth


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
        return tuple(decoded_base64_authorization_header.split(':'))
