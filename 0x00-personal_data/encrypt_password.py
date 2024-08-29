#!/usr/bin/env python3
"""
Encrypting passwords, user passwords should never be stored
in plain text in database
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    returns a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validates that the provided password matched the hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
