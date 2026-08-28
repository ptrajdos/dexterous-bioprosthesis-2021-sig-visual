"""Application settings module.

Defines root directory and data path constants used across the application.
"""

import os

ROOT = os.path.abspath(os.path.dirname(__file__))
"""Absolute path to the package root directory."""

DATAPATH = os.path.join(ROOT, "../", "data")
"""Absolute path to the data directory."""
