#!/usr/bin/env python3
"""auth module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes a password"""
    return bcrypt.hashpw(bytes(password, 'utf-8'),
                         bcrypt.gensalt())
