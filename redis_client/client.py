"""
Redis Client Module
High-level Redis client with organized operations
"""
from typing import Optional, List, Dict, Any
import redis

from .config import RedisConfig
from .connection import RedisConnection
from .operations import (
    KeyTypeChecker,
    StringOperations,
    ListOperations,
    HashOperations,
    SetOperations
)


class RedisClient:
    """
    High-level Redis client with organized operations
    Provides a clean interface for Redis operations
    """
    
    def __init__(self, config: RedisConfig):
        """
        Initialize Redis client
        
        Args:
            config: RedisConfig instance
        """
        self.config = config
        self._connection = RedisConnection(config)
        self._connection.connect()
        
        # Initialize operation handlers
        self._client = self._connection.client #sudah memiliki object redis  Optional[redis_client.Redis] = None
        self.type_checker = KeyTypeChecker(self._client)
        self.string = StringOperations(self._client)
        self.list = ListOperations(self._client)
        self.hash = HashOperations(self._client)
        self.set = SetOperations(self._client)
    
    @classmethod
    def from_env(cls, REDIS_ADDR: str, REDIS_PORT: int, REDIS_PASSWORD: str) -> "RedisClient":
        """
        Create Redis client from environment variables

        Args:
            REDIS_ADDR: Redis address
            REDIS_PORT: Redis port
            REDIS_PASSWORD: Redis password
            
        Returns:
            RedisClient instance
        """
        config = RedisConfig.from_env(REDIS_ADDR, REDIS_PORT, REDIS_PASSWORD)
        return cls(config)
    
    @property
    def client(self) -> redis.Redis:
        """Get underlying Redis client"""
        return self._client
    
    def ping(self) -> bool:
        """
        Test connection to Redis server
        
        Returns:
            True if connected
        """
        return self._client.ping() #<-- langsung dari library redis pingnya
    
    def get_key_type(self, key: str) -> str:
        """
        Get the type of a Redis key
        
        Args:
            key: Redis key
            
        Returns:
            Key type as string
        """
        return self.type_checker.get_type(key)
    
    def key_exists(self, key: str) -> bool:
        """
        Check if key exists
        
        Args:
            key: Redis key
            
        Returns:
            True if key exists
        """
        return self._client.exists(key) > 0 #<-- langsung dari library redis existsnya
    
    def delete_key(self, *keys: str) -> int:
        """
        Delete one or more keys
        
        Args:
            keys: Redis keys to delete
            
        Returns:
            Number of keys deleted
        """
        return self._client.delete(*keys)
    
    def get_value_by_type(self, key: str) -> Optional[Any]:
        """
        Get value based on key type
        
        Args:
            key: Redis key
            
        Returns:
            Value based on type, or None if key doesn't exist
        """
        key_type = self.get_key_type(key)
        
        if key_type == "string":
            return self.string.get(key)
        elif key_type == "list":
            return self.list.lrange(key)
        elif key_type == "hash":
            return self.hash.hgetall(key)
        elif key_type == "set":
            return self.set.smembers(key)
        elif key_type == "none":
            return None
        else:
            return f"Unsupported type: {key_type}"
    
    def close(self) -> None:
        """Close Redis connection"""
        self._connection.disconnect()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

