#!/usr/bin/env python3
"""
obfuscating sensitive data
"""
import mysql.connector
import os
import re
from typing import List, Optional, Union
import logging

PII_FIELDS = ("email", 'name', "ssn", "password", "phone")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        initialize formatter with with sensitive fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = [] if len(fields) == 0 else fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formats a log record while obfuscating sensitive fields
        """
        message = filter_datum(self.fields, self.REDACTION,
                               record.getMessage(), self.SEPARATOR)
        record.msg = message
        formatted_message = super().format(record)
        return formatted_message


def get_logger() -> logging.Logger:
    """
    returns:loggin.Logger object.
    The logger should be named "user_data" and
    only log up to logging.INFO level. It should not propagate messages
    to other loggers. It should have a StreamHandler
    with RedactingFormatter as formatter
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamhandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns: connector to the database (
    mysql.connector.connection.MySQLConnection object)
    """
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    connector = mysql.connector.connection.MySQLConnection(user=user,
                                                           password=password,
                                                           host=host,
                                                           database=database)
    return connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    obfuscates a log message (message)
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
        all fields in
        the log line (message)
    returns: the log message obfuscated
    """
    return re.sub(
        r'([^{}]*=[^{}]*){}'.format(separator, separator, separator), lambda
        match: re.sub(r'=.+', f'={redaction}{separator}', match.group(0))
        if match.group(0).split('=')[0] in fields else match.group(0), message)
