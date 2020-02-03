#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

"""
This module provides error codes used in the project.
These codes should be used to return to the system
or as results for methods in the project.
"""

from enum import IntEnum, auto, unique

@unique
class ErrorCode(IntEnum):
    """
    The error codes for this program.
    """
    OK = 0
    UNKNOWN_COMMAND = auto()
    MISSING_ARGUMENT = auto()
    TOO_FEW_ARGUMENTS = auto()
    FILE_ERROR = auto()
    COMMAND_FAILED = auto()
    SMTP_ERROR = auto()
    UNKNOWN_ERROR = 666
