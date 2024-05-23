#!/usr/bin/env python3
"""auth module has the class Auth"""
from flask import request
from typing import TypeVar, List


class Auth:
    """manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """
        request will be the Flask request object
        returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None
        request will be the Flask request object
        """
        return None
