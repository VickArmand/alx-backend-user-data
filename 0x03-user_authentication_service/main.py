#!/usr/bin/env python3
"""main module"""
import requests


def register_user(email: str, password: str) -> None:
    """"""
    response = requests.post('http://localhost:5000/users',
                             {"email": email,
                              "password": password})
    if response.status_code == 200:
        expected_response = {"email": email, "message": "user created"}
        assert response.json() == expected_response
    else:
        assert response.status_code == 400
        expected_response = {'message': 'email already registered'}
        assert response.json() == expected_response


def log_in_wrong_password(email: str, password: str) -> None:
    """"""
    response = requests.post('http://localhost:5000/sessions',
                             {"email": email,
                              "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """"""
    response = requests.post('http://localhost:5000/sessions',
                             {"email": email,
                              "password": password})
    if response.status_code == 200:
        expected_response = {"email": email, "message": "logged in"}
        assert response.json() == expected_response
        return response.cookies.get("session_id")
    assert response.status_code == 401


def profile_unlogged() -> None:
    """"""
    response = requests.get('http://localhost:5000/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """"""
    response = requests.get('http://localhost:5000/profile',
                            cookies={'session_id': session_id})
    assert response.status_code == 200
    expected_response = {'email': EMAIL}
    assert response.json() == expected_response


def log_out(session_id: str) -> None:
    """"""
    response = requests.delete('http://localhost:5000/sessions',
                               cookies={'session_id': session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """"""
    response = requests.post('http://localhost:5000/reset_password',
                             {"email": email})
    assert response.status_code == 200
    token = response.json()['reset_token']
    expected_response = {"email": email, "reset_token": token}
    assert response.json() == expected_response
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """"""
    params = {"email": email,
              "reset_token": reset_token,
              "new_password": new_password}
    response = requests.put('http://localhost:5000/reset_password',
                            params)
    if response.status_code == 200:
        assert response.json() == {"email": email,
                                   "message": "Password updated"}
    else:
        assert response.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
