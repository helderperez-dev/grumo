"""Grumo style adapters.

The native Grumo CSS adapter is the default; Tailwind is opt-in::

    from grumo import TailwindAdapter, set_style_adapter
    set_style_adapter(TailwindAdapter())
"""

from grumo.adapters.capabilities import (
    AdapterCapabilities,
    CapabilityError,
    DatabaseCapabilities,
    EventBusCapabilities,
    ObjectStoreCapabilities,
    QueueCapabilities,
    capability_matrix,
    negotiate,
    require,
)
from grumo.adapters.registry import ProviderRegistry, registry
from grumo.adapters.tailwind import TailwindAdapter
from grumo.adapters.grumo_css import GrumoCSSAdapter, generate_component_css

__all__ = [
    "TailwindAdapter",
    "GrumoCSSAdapter",
    "generate_component_css",
    "AdapterCapabilities",
    "CapabilityError",
    "DatabaseCapabilities",
    "EventBusCapabilities",
    "ObjectStoreCapabilities",
    "QueueCapabilities",
    "capability_matrix",
    "negotiate",
    "require",
    "ProviderRegistry",
    "registry",
]
