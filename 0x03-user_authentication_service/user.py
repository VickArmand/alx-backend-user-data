#!/usr/bin/env python3
"""user module"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()


class User(Base):
    """
    model named User for a database table
    named users (by using the mapping
    declaration of SQLAlchemy).
    The model will have the following attributes:
        id, the integer primary key
        email, a non-nullable string
        hashed_password, a non-nullable string
        session_id, a nullable string
        reset_token, a nullable string
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_password = Column(String(250))
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
