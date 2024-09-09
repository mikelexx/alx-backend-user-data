#!/usr/bin/env python3
"""
hashing password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    returns a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
