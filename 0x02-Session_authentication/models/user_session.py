#!/usr/bin/env python3
""" user_session module
"""
from models.base import Base


class UserSession(Base):
    """inherits from Base"""

    def __init__(self, *args: list,
                 user_id: str,
                 session_id: str,
                 **kwargs: dict):
        """initialize"""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.user_id = user_id
        self.session_id = session_id
