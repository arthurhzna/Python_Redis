"""
Redis Package
Clean OOP implementation for Redis operations
"""

from .config import RedisConfig
from .connection import RedisConnection
from .client import RedisClient
from .operations import (
    StringOperations,
    ListOperations,
    HashOperations,
    SetOperations,
    KeyTypeChecker
)

__all__ = [
    "RedisConfig",
    "RedisConnection",
    "RedisClient",
    "StringOperations",
    "ListOperations",
    "HashOperations",
    "SetOperations",
    "KeyTypeChecker"
]

__version__ = "1.0.0"

