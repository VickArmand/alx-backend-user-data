#!/usr/bin/env python3
"""session_auth module"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[id] = user_id
        return id
