# Redis OOP Package

Clean, well-structured Object-Oriented Programming implementation for Redis operations in Python.

## Architecture

The package follows SOLID principles and is organized into several modules:

### Module Structure

```
redis/
├── __init__.py          # Package initialization and exports
├── config.py            # Configuration management
├── connection.py        # Connection lifecycle management
├── operations.py        # Type-specific operations
├── client.py            # High-level client interface
└── README.md           # Documentation
```

### Components

#### 1. **RedisConfig** (`config.py`)
- Manages Redis connection configuration
- Loads settings from environment variables
- Validates configuration parameters

#### 2. **RedisConnection** (`connection.py`)
- Handles connection lifecycle
- Supports context manager protocol
- Provides connection health checks

#### 3. **Operations** (`operations.py`)
- `StringOperations`: String data type operations
- `ListOperations`: List data type operations
- `HashOperations`: Hash data type operations
- `SetOperations`: Set data type operations
- `KeyTypeChecker`: Utility for checking key types

#### 4. **RedisClient** (`client.py`)
- High-level interface combining all operations
- Provides convenient methods for common tasks
- Supports context manager for automatic cleanup

## Usage Examples

### Basic Usage

```python
from redis import RedisClient

# Initialize client from environment variables
client = RedisClient.from_env(".env")

# Test connection
client.ping()

# Get key type
key_type = client.get_key_type("my_key")

# String operations
client.string.set("name", "John")
value = client.string.get("name")

# List operations
client.list.rpush("queue", "item1", "item2")
item = client.list.lpop("queue")

# Close connection
client.close()
```

### Using Context Manager

```python
from redis import RedisClient

with RedisClient.from_env(".env") as client:
    # Operations here
    client.list.rpush("queue", "data")
    item = client.list.lpop("queue")
    # Connection automatically closed
```

### String Operations

```python
# Set value
client.string.set("key", "value")

# Set with expiration (in seconds)
client.string.set("key", "value", ex=3600)

# Get value
value = client.string.get("key")

# Delete key
client.string.delete("key")
```

### List Operations

```python
# Push to right
client.list.rpush("queue", "item1", "item2")

# Push to left
client.list.lpush("queue", "item0")

# Pop from left
item = client.list.lpop("queue")

# Pop from right
item = client.list.rpop("queue")

# Get all items
items = client.list.lrange("queue", 0, -1)

# Get list length
length = client.list.llen("queue")
```

### Hash Operations

```python
# Set field
client.hash.hset("user:1", "name", "John")

# Get field
name = client.hash.hget("user:1", "name")

# Get all fields
user_data = client.hash.hgetall("user:1")

# Delete fields
client.hash.hdel("user:1", "name", "email")
```

### Set Operations

```python
# Add members
client.set.sadd("tags", "python", "redis", "oop")

# Get all members
tags = client.set.smembers("tags")

# Remove members
client.set.srem("tags", "python")
```

## Environment Variables

Create a `.env` file with the following variables:

```env
REDIS_ADDR=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password_here
```

## Design Principles

### 1. **Single Responsibility Principle (SRP)**
Each class has a single, well-defined responsibility:
- `RedisConfig`: Configuration management
- `RedisConnection`: Connection management
- `StringOperations`: String operations only
- etc.

### 2. **Open/Closed Principle (OCP)**
The design is open for extension but closed for modification. New operation types can be added without modifying existing code.

### 3. **Dependency Inversion Principle (DIP)**
High-level modules depend on abstractions, not concrete implementations.

### 4. **Separation of Concerns**
- Configuration is separate from connection management
- Connection management is separate from operations
- Each data type has its own operation class

## Benefits

1. **Clean Code**: Easy to read and understand
2. **Maintainable**: Changes are localized to specific modules
3. **Testable**: Each component can be tested independently
4. **Reusable**: Components can be used in different contexts
5. **Type-Safe**: Clear interfaces and type hints
6. **Documented**: Comprehensive docstrings for all public methods

## Error Handling

The package includes proper error handling:
- Configuration validation
- Connection error handling
- Type checking for operations

## Testing

Each component can be tested independently:

```python
# Test configuration
config = RedisConfig.from_env(".env")
assert config.host == "localhost"

# Test connection
connection = RedisConnection(config)
assert connection.is_connected()

# Test operations
client = RedisClient(config)
client.string.set("test", "value")
assert client.string.get("test") == "value"
```

