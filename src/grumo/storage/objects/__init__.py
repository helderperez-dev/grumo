"""Object storage capability.

Grumo Store is the canonical local-first object backend. Local filesystem and
S3 implementations remain explicit compatibility/infrastructure adapters.
"""

from grumo.storage.objects.interfaces import GrumoObjectStore
from grumo.storage.objects.local import LocalObjectStore
from grumo.storage.objects.s3 import S3ObjectStore
from grumo.storage.objects.store import GrumoStoreObjectStore

__all__ = [
    "GrumoObjectStore",
    "GrumoStoreObjectStore",
    "LocalObjectStore",
    "S3ObjectStore",
]
