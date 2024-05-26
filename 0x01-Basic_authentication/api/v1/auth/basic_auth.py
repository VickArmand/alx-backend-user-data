#!/usr/bin/env python3
"""
basic_auth module
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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
        except binascii.Error:
            return None
