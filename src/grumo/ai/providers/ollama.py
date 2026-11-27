"""Compatibility alias for :mod:`grumo.integrations.ai.ollama`."""

import sys

from grumo.integrations.ai import ollama

sys.modules[__name__] = ollama
