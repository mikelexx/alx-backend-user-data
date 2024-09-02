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
        returns the Base64 part of the Authorization header for
        a Basic Authentication
        """
        if not authorization_header \
                or type(authorization_header) is not str \
                or not authorization_header.startswith('Basic '):
            return
        return authorization_header.split(' ')[1]
