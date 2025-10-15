"""
Redis Connection Module
Manages Redis client connection lifecycle
"""
import redis
from typing import Optional
from .config import RedisConfig


class RedisConnection:
    """Manages Redis client connection"""
    
    def __init__(self, config: RedisConfig):
        """
        Initialize Redis connection
        
        Args:
            config: RedisConfig instance
        """
        self.config = config
        self._client: Optional[redis.Redis] = None
    
    def connect(self) -> redis.Redis:
        """
        Establish connection to Redis server
        
        Returns:
            Redis client instance
            
        Raises:
            redis.ConnectionError: If connection fails
        """
        if self._client is None:
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                password=self.config.password,
                decode_responses=self.config.decode_responses
            )
            # Test connection
            self._client.ping()
        
        return self._client
    
    @property
    def client(self) -> redis.Redis:
        """
        Get Redis client, connecting if necessary
        
        Returns:
            Redis client instance
        """
        if self._client is None:
            return self.connect()
        return self._client
    
    def disconnect(self) -> None:
        """Close Redis connection"""
        if self._client is not None:
            self._client.close()
            self._client = None
    
    def is_connected(self) -> bool:
        """
        Check if connection is active
        
        Returns:
            True if connected, False otherwise
        """
        if self._client is None:
            return False
        
        try:
            self._client.ping()
            return True
        except redis.ConnectionError:
            return False
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

