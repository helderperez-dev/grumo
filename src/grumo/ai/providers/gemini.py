"""Compatibility alias for :mod:`grumo.integrations.ai.gemini`."""

import sys

from grumo.integrations.ai import gemini

sys.modules[__name__] = gemini
