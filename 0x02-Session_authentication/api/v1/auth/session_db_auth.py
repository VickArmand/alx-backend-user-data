#!/usr/bin/env python3
""" session_db_auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """inherits from SessionExpAuth"""

    def create_session(self, user_id=None):
        """ creates and stores new instance of UserSession
        and returns the Session ID"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        obj = UserSession(user_id=user_id, session_id=session_id)
        obj.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession
        in the database based on session_id"""
        if session_id is None:
            return None
        users_sessions = UserSession.search({'session_id': session_id})
        if len(users_sessions) == 0:
            return None
        if self.session_duration <= 0:
            return users_sessions[0].user_id
        created_at = users_sessions[0]['created_at']
        if created_at + timedelta(seconds=self.session_duration
                                  ) < datetime.now():
            return None
        return users_sessions[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID
        from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return False
        user_sessions[0].remove()
        return True
