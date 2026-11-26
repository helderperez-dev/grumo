"""Compatibility alias for :mod:`grumo.integrations.ai.openai`."""

import sys

from grumo.integrations.ai import openai

sys.modules[__name__] = openai
