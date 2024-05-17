#!/usr/bin/env python3
"""
This module has a function called filter_datum
that returns an obfuscated log message
"""
import re
import logging
from typing import List
PII_FIELDS = ('name',
              'email',
              'phone',
              'ssn',
              'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records
        using filter_datum
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,
                            RedactingFormatter.REDACTION,
                            message,
                            RedactingFormatter.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character
        is separating all fields in the log line (message)
    The function should use a regex to replace occurrences
    of certain field values.
    filter_datum should be less than 5 lines long and use re.sub
    to perform the substitution with a single regex.
    """
    for field in fields:
        message = re.sub(f"{field}=[^;]+;",
                         f"{field}={redaction}{separator}",
                         message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamhandler)
    logger.propagate = False
    return logger
