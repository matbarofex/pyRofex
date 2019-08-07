# -*- coding: utf-8 -*-
"""
    pyRofex.components.exceptions

    Defines all library exceptions
"""


class ApiException(Exception):
    """
    Represent a controlled exception raised by the library.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

