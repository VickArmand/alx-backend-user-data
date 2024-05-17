#!/usr/bin/env python3
"""
This module has a function called filter_datum
that returns an obfuscated log message
"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
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
