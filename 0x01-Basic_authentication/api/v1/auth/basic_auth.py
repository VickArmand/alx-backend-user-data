#!/usr/bin/env python3
"""
basic_auth module
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        for a Basic Authentication"""
        if authorization_header is None:
            return None
        elif type(authorization_header) != str:
            return None
        elif authorization_header[0:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of
        a Base64 string base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) != str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from
        the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        elif type(decoded_base64_authorization_header) != str:
            return None, None
        elif ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':')
        return credentials[0], credentials[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or user_pwd is None:
            return None
        elif type(user_email) != str or type(user_pwd) != str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users or len(users) == 0:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and
        retrieves the User instance for a request"""
        header = self.authorization_header(request)
        header_extract = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(
            header_extract)
        credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(credentials[0],
                                                 credentials[1])
