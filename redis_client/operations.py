"""
Redis Operations Module
Provides high-level operations for different Redis data types
"""
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import redis


class RedisOperation(ABC):
    """Abstract base class for Redis operations"""
    
    def __init__(self, client: redis.Redis):
        """
        Initialize operation with Redis client
        
        Args:
            client: Redis client instance
        """
        self.client = client
    
    @abstractmethod
    def execute(self, key: str) -> Any:
        """
        Execute the operation
        
        Args:
            key: Redis key
            
        Returns:
            Operation result
        """
        pass


class KeyTypeChecker:
    """Utility class for checking Redis key types"""
    
    def __init__(self, client: redis.Redis):
        self.client = client
    
    def get_type(self, key: str) -> str:
        """
        Get the type of a Redis key
        
        Args:
            key: Redis key
            
        Returns:
            Key type as string (string, list, set, zset, hash, none)
        """
        key_type = self.client.type(key)
        return key_type.decode() if isinstance(key_type, bytes) else key_type


class StringOperations:
    """Operations for Redis string data type"""
    
    def __init__(self, client: redis.Redis):
        self.client = client
    
    def get(self, key: str) -> Optional[str]:
        """
        Get string value
        
        Args:
            key: Redis key
            
        Returns:
            String value or None if key doesn't exist
        """
        return self.client.get(key)
    
    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """
        Set string value
        
        Args:
            key: Redis key
            value: String value to set
            ex: Expiration time in seconds (optional)
            
        Returns:
            True if successful
        """
        return self.client.set(key, value, ex=ex)
    
    def delete(self, key: str) -> int:
        """
        Delete key
        
        Args:
            key: Redis key
            
        Returns:
            Number of keys deleted
        """
        return self.client.delete(key)


class ListOperations:
    """Operations for Redis list data type"""
    
    def __init__(self, client: redis.Redis):
        self.client = client
    
    def lpush(self, key: str, *values: str) -> int:
        """
        Push values to the left of the list
        
        Args:
            key: Redis key
            values: Values to push
            
        Returns:
            Length of list after push
        """
        return self.client.lpush(key, *values)
    
    def rpush(self, key: str, *values: str) -> int:
        """
        Push values to the right of the list
        
        Args:
            key: Redis key
            values: Values to push
            
        Returns:
            Length of list after push
        """
        return self.client.rpush(key, *values)
    
    def lpop(self, key: str) -> Optional[str]:
        """
        Pop value from the left of the list
        
        Args:
            key: Redis key
            
        Returns:
            Popped value or None if list is empty
        """
        return self.client.lpop(key)
    
    def rpop(self, key: str) -> Optional[str]:
        """
        Pop value from the right of the list
        
        Args:
            key: Redis key
            
        Returns:
            Popped value or None if list is empty
        """
        return self.client.rpop(key)
    
    def lrange(self, key: str, start: int = 0, end: int = -1) -> List[str]:
        """
        Get range of values from list
        
        Args:
            key: Redis key
            start: Start index
            end: End index (-1 for all)
            
        Returns:
            List of values
        """
        return self.client.lrange(key, start, end)
    
    def llen(self, key: str) -> int:
        """
        Get length of list
        
        Args:
            key: Redis key
            
        Returns:
            Length of list
        """
        return self.client.llen(key)


class HashOperations:
    """Operations for Redis hash data type"""
    
    def __init__(self, client: redis.Redis):
        self.client = client
    
    def hset(self, key: str, field: str, value: str) -> int:
        """
        Set hash field
        
        Args:
            key: Redis key
            field: Hash field
            value: Field value
            
        Returns:
            1 if new field, 0 if updated
        """
        return self.client.hset(key, field, value)
    
    def hget(self, key: str, field: str) -> Optional[str]:
        """
        Get hash field value
        
        Args:
            key: Redis key
            field: Hash field
            
        Returns:
            Field value or None
        """
        return self.client.hget(key, field)
    
    def hgetall(self, key: str) -> Dict[str, str]:
        """
        Get all hash fields and values
        
        Args:
            key: Redis key
            
        Returns:
            Dictionary of field-value pairs
        """
        return self.client.hgetall(key)
    
    def hdel(self, key: str, *fields: str) -> int:
        """
        Delete hash fields
        
        Args:
            key: Redis key
            fields: Fields to delete
            
        Returns:
            Number of fields deleted
        """
        return self.client.hdel(key, *fields)


class SetOperations:
    """Operations for Redis set data type"""
    
    def __init__(self, client: redis.Redis):
        self.client = client
    
    def sadd(self, key: str, *members: str) -> int:
        """
        Add members to set
        
        Args:
            key: Redis key
            members: Members to add
            
        Returns:
            Number of members added
        """
        return self.client.sadd(key, *members)
    
    def smembers(self, key: str) -> set:
        """
        Get all set members
        
        Args:
            key: Redis key
            
        Returns:
            Set of members
        """
        return self.client.smembers(key)
    
    def srem(self, key: str, *members: str) -> int:
        """
        Remove members from set
        
        Args:
            key: Redis key
            members: Members to remove
            
        Returns:
            Number of members removed
        """
        return self.client.srem(key, *members)

