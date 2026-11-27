"""Compatibility alias for :mod:`grumo.integrations.ai.anthropic`."""

import sys

from grumo.integrations.ai import anthropic

sys.modules[__name__] = anthropic
