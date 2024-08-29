#!/usr/bin/env python3
"""
Encrypting passwords, user passwords should never be stored
in plain text in database
"""
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """
    returns a salted, hashed password, which is a byte string.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
