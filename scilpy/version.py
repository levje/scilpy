# -*- coding: utf-8 -*-

import importlib.metadata

__version__ = importlib.metadata.version("mypackage")
version_string = "\nScilpy version: " + __version__
