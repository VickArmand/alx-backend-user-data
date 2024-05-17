#!/usr/bin/env python3
"""encrypt_password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    expects one string argument name password and
    returns a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Use bcrypt to validate that the
    provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
