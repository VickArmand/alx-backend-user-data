#!/usr/bin/env python3
"""auth module"""
import bcrypt
import uuid
from db import DB, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashes a password"""
    return bcrypt.hashpw(bytes(password, 'utf-8'),
                         bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialize"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def create_session(self, email: str) -> str:
        """
        It takes an email string argument
        and returns the session ID as a string.
        The method should find the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user’s session_id, then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        takes a single session_id string argument
        and returns the corresponding User or None.
        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user.
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except (NoResultFound, InvalidRequestError):
                return None
        return None

    def destroy_session(self, user_id: str):
        """
        The method takes a single user_id integer argument
        and returns None.
        The method updates the corresponding
        user’s session ID to None.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user.session_id:
                self._db.update_user(user_id, session_id=None)
        except (NoResultFound, InvalidRequestError):
            pass
        finally:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        take an email string argument and returns a string.
        Find the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID
        and update the user’s reset_token database field.
        Return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            user = None
        if user is not None:
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        raise ValueError
