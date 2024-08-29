#!/usr/bin/env python3
"""
obfuscating sensitive data
"""
import re
from typing import List, Optional, Union

import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Optional[List[str]] = None):
        """
        initialize formatter with with sensitive fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = [] if fields is None else fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formats a log record while obfuscating sensitive fields
        """
        return filter_datum(self.fields, self.REDACTION, record.getMessage(),
                            self.SEPARATOR)


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
