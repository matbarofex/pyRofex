# -*- coding: utf-8 -*-
"""
    pyRofex.components.globals

    Defines library global variables
"""

import ssl

from .enums import Environment

# Default environment used if None environment is specified.
default_environment = None

# Environment specific configuration.
environment_config = {
    Environment.REMARKET: {
        "url": "https://api.remarkets.primary.com.ar/",
        "ws": "wss://api.remarkets.primary.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": None,
        "ws_client": None,
        "token": None,
        "user": None,
        "password": None,
        "account": None,
        "initialized": False,
        "proprietary": "PBCP",
        "heartbeat": 30,
        "ssl_opt": None
    },
    Environment.LIVE: {
        "url": "https://api.primary.com.ar/",
        "ws": "wss://api.primary.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": None,
        "ws_client": None,
        "user": None,
        "password": None,
        "account": None,
        "initialized": False,
        "proprietary": "api",
        "heartbeat": 30,
        "ssl_opt": None
    }
}
