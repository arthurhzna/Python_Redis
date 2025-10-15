# Architecture Documentation

## System Overview

The Redis OOP package is designed with a layered architecture following SOLID principles.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│                   (main.py, examples.py)                 │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   High-Level Client                      │
│                    (RedisClient)                         │
│  - Unified interface for all operations                 │
│  - Context manager support                              │
│  - Type detection and routing                           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Operations Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   String    │  │    List     │  │    Hash     │    │
│  │ Operations  │  │ Operations  │  │ Operations  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐                      │
│  │     Set     │  │    Type     │                      │
│  │ Operations  │  │   Checker   │                      │
│  └─────────────┘  └─────────────┘                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Connection Layer                         │
│                 (RedisConnection)                        │
│  - Connection lifecycle management                      │
│  - Health checks                                        │
│  - Resource cleanup                                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                Configuration Layer                       │
│                  (RedisConfig)                          │
│  - Environment variable loading                         │
│  - Configuration validation                             │
│  - Default values                                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Redis Server                           │
└─────────────────────────────────────────────────────────┘
```

## Component Relationships

```
RedisConfig ──────> RedisConnection ──────> RedisClient
                                                  │
                                                  ├──> StringOperations
                                                  ├──> ListOperations
                                                  ├──> HashOperations
                                                  ├──> SetOperations
                                                  └──> KeyTypeChecker
```

## Class Diagram

```
┌─────────────────────────┐
│     RedisConfig         │
├─────────────────────────┤
│ + host: str             │
│ + port: int             │
│ + password: str?        │
│ + decode_responses: bool│
├─────────────────────────┤
│ + from_env()            │
└─────────────────────────┘
           │
           │ uses
           ▼
┌─────────────────────────┐
│   RedisConnection       │
├─────────────────────────┤
│ - config: RedisConfig   │
│ - _client: Redis?       │
├─────────────────────────┤
│ + connect()             │
│ + disconnect()          │
│ + is_connected()        │
│ + __enter__()           │
│ + __exit__()            │
└─────────────────────────┘
           │
           │ provides client to
           ▼
┌─────────────────────────┐
│     RedisClient         │
├─────────────────────────┤
│ - _connection           │
│ - _client: Redis        │
│ + string: StringOps     │
│ + list: ListOps         │
│ + hash: HashOps         │
│ + set: SetOps           │
│ + type_checker          │
├─────────────────────────┤
│ + from_env()            │
│ + ping()                │
│ + get_key_type()        │
│ + key_exists()          │
│ + delete_key()          │
│ + get_value_by_type()   │
│ + close()               │
└─────────────────────────┘
           │
           │ delegates to
           ▼
┌─────────────────────────┐
│   StringOperations      │
├─────────────────────────┤
│ - client: Redis         │
├─────────────────────────┤
│ + get(key)              │
│ + set(key, value)       │
│ + delete(key)           │
└─────────────────────────┘

┌─────────────────────────┐
│    ListOperations       │
├─────────────────────────┤
│ - client: Redis         │
├─────────────────────────┤
│ + lpush(key, values)    │
│ + rpush(key, values)    │
│ + lpop(key)             │
│ + rpop(key)             │
│ + lrange(key, s, e)     │
│ + llen(key)             │
└─────────────────────────┘

┌─────────────────────────┐
│    HashOperations       │
├─────────────────────────┤
│ - client: Redis         │
├─────────────────────────┤
│ + hset(key, field, val) │
│ + hget(key, field)      │
│ + hgetall(key)          │
│ + hdel(key, fields)     │
└─────────────────────────┘

┌─────────────────────────┐
│    SetOperations        │
├─────────────────────────┤
│ - client: Redis         │
├─────────────────────────┤
│ + sadd(key, members)    │
│ + smembers(key)         │
│ + srem(key, members)    │
└─────────────────────────┘
```

## Design Patterns

### 1. **Facade Pattern**
`RedisClient` provides a simplified interface to the complex Redis operations.

### 2. **Strategy Pattern**
Different operation classes (`StringOperations`, `ListOperations`, etc.) implement different strategies for handling Redis data types.

### 3. **Factory Pattern**
`RedisConfig.from_env()` and `RedisClient.from_env()` are factory methods.

### 4. **Context Manager Pattern**
Both `RedisConnection` and `RedisClient` implement `__enter__` and `__exit__` for resource management.

### 5. **Dependency Injection**
Operation classes receive the Redis client as a dependency, not creating it themselves.

## Data Flow

### Example: Setting a String Value

```
User Code
    │
    ▼
client.string.set("key", "value")
    │
    ▼
StringOperations.set()
    │
    ▼
redis.Redis.set()
    │
    ▼
Redis Server
```

### Example: Popping from List

```
User Code
    │
    ▼
client.list.lpop("queue")
    │
    ▼
ListOperations.lpop()
    │
    ▼
redis.Redis.lpop()
    │
    ▼
Redis Server
    │
    ▼
Return value
```

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- `RedisConfig`: Only handles configuration
- `RedisConnection`: Only manages connection lifecycle
- `StringOperations`: Only handles string operations
- Each class has one reason to change

### Open/Closed Principle (OCP)
- New operation types can be added without modifying existing code
- Extend by adding new operation classes
- Closed for modification, open for extension

### Liskov Substitution Principle (LSP)
- All operation classes can be used interchangeably where their base behavior is expected
- Subclasses maintain the contract of their base abstractions

### Interface Segregation Principle (ISP)
- Operation classes provide focused interfaces
- Clients only depend on methods they use
- No "fat" interfaces

### Dependency Inversion Principle (DIP)
- High-level `RedisClient` depends on abstractions (operation interfaces)
- Low-level modules (operations) implement these abstractions
- Both depend on abstractions, not concretions

## Error Handling Strategy

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  - Business logic error handling        │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Client Layer                    │
│  - Validates inputs                     │
│  - Provides meaningful error messages   │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│       Operations Layer                  │
│  - Handles operation-specific errors    │
│  - Returns None for missing keys        │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│       Connection Layer                  │
│  - Handles connection errors            │
│  - Manages reconnection logic           │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      Configuration Layer                │
│  - Validates configuration              │
│  - Raises ValueError for invalid config │
└─────────────────────────────────────────┘
```

## Extension Points

### Adding New Data Type Operations

1. Create new operation class in `operations.py`:
```python
class SortedSetOperations:
    def __init__(self, client: redis.Redis):
        self.client = client
    
    def zadd(self, key: str, mapping: dict) -> int:
        return self.client.zadd(key, mapping)
```

2. Add to `RedisClient` in `client.py`:
```python
self.zset = SortedSetOperations(self._client)
```

3. Export in `__init__.py`:
```python
from .operations import SortedSetOperations

__all__ = [..., "SortedSetOperations"]
```

### Adding Custom Methods

Extend `RedisClient` with domain-specific methods:
```python
class CustomRedisClient(RedisClient):
    def process_image_queue(self, queue_key: str):
        # Custom business logic
        pass
```

## Testing Strategy

```
Unit Tests
    │
    ├── Config Tests
    │   └── Test environment loading
    │   └── Test validation
    │
    ├── Connection Tests
    │   └── Test connect/disconnect
    │   └── Test health checks
    │
    ├── Operation Tests
    │   └── Test each operation class
    │   └── Mock Redis client
    │
    └── Integration Tests
        └── Test full workflow
        └── Test with real Redis
```

## Performance Considerations

1. **Connection Pooling**: Redis-py handles connection pooling internally
2. **Pipelining**: Can be added for batch operations
3. **Lazy Connection**: Connection only established when needed
4. **Resource Cleanup**: Context managers ensure proper cleanup

## Security Considerations

1. **Password Protection**: Passwords loaded from environment variables
2. **No Hardcoded Credentials**: All config from .env file
3. **Connection Encryption**: Can be added via SSL/TLS configuration
4. **Input Validation**: Configuration validated before use

