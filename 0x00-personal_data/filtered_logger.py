#!/usr/bin/env python3
"""
obfuscating sensitive data
"""
import re
from typing import List


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
