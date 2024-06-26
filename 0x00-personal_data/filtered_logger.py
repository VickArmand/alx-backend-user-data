#!/usr/bin/env python3
"""
This module has a function called filter_datum
that returns an obfuscated log message
"""
import re
import logging
import os
import mysql.connector
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(host=host,
                                   user=user,
                                   password=password,
                                   database=db)


def main() -> None:
    """
    The function will obtain a database connection using get_db and
    retrieve all rows in the users table and display each row
    """
    db = get_db()
    cursor = db.cursor()
    fields = ('name', 'email', 'phone', 'ssn', 'password',
              'ip', 'last_login', 'user_agent')
    columns = 'name, email, phone, ssn, password, ip, last_login, user_agent'
    query = f"SELECT {columns} FROM users"
    cursor.execute(query)
    results = cursor.fetchall()
    logger = get_logger()
    for result in results:
        log = ''
        for i in range(len(fields)):
            log += f'{fields[i]}={result[i]};'
        logger.info(RedactingFormatter(PII_FIELDS).format(log))
    cursor.close()


if __name__ == "__main__":
    main()
