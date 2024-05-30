#!/usr/bin/env python3
"""auth module"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashes a password"""
    return bcrypt.hashpw(bytes(password, 'utf-8'),
                         bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialize"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """
        If a user already exist with the passed email,
        raise a ValueError with the message
        User <user's email> already exists.
        If not, hash the password with _hash_password,
        save the user to the database using self._db and
        return the User object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """validates credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False
