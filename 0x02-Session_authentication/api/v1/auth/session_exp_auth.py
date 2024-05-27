#!/usr/bin/env python3
""" session_exp_auth module
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """inherits from SessionAuth"""

    def __init__(self):
        """initialize"""
        try:
            duration = int(os.getenv('SESSION_DURATION'))
            self.session_duration = duration
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """"""
        session = super().create_session(user_id)
        if not session:
            return None
        session_dictionary = {'user_id': user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session] = session_dictionary
        return session

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        session_dict = self.user_id_for_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.user_id
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(seconds=self.session_duration
                                  ) < datetime.now():
            return None
        return session_dict.user_id
