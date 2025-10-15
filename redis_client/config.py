"""
Redis Configuration Module
Handles loading and managing Redis connection configuration
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class RedisConfig:
    """Redis connection configuration"""
    host: str
    port: int
    password: Optional[str] = None
    decode_responses: bool = True
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "RedisConfig":
        """
        Load Redis configuration from environment variables
        
        Args:
            env_file: Path to .env file
            
        Returns:
            RedisConfig instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        load_dotenv(env_file, override=True)
        
        host = os.getenv("REDIS_ADDR")
        port = os.getenv("REDIS_PORT")
        password = os.getenv("REDIS_PASSWORD")
        
        if not host:
            raise ValueError("REDIS_ADDR environment variable is required")
        if not port:
            raise ValueError("REDIS_PORT environment variable is required")
        
        try:
            port_int = int(port)
        except ValueError:
            raise ValueError(f"REDIS_PORT must be a valid integer, got: {port}")
        
        return cls(
            host=host,
            port=port_int,
            password=password if password else None
        )

