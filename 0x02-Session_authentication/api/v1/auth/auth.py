#!/usr/bin/env python3
"""auth module has the class Auth"""
from flask import request
from typing import TypeVar, List
import re


class Auth:
    """manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        You can assume excluded_paths contains
        string path always ending by a /
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        pattern = ''
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                pattern = f'{excluded_path[0:-1]}.*'
            elif excluded_path[-1] == '/':
                pattern = f'{excluded_path[0:-1]}/*'
            else:
                pattern = f'{excluded_path[0:-1]}/*'
            match_obj = re.match(pattern, path)
            if match_obj:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        request will be the Flask request object
        returns None
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None
        request will be the Flask request object
        """
        return None
