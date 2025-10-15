"""
Main module demonstrating Redis operations using clean OOP structure
"""
from redis_client import RedisClient


def main():
    """Main function to demonstrate Redis operations"""
    
    # Initialize Redis client from environment variables
    client = RedisClient.from_env(".env")
    
    # Test connection
    print("Testing connection...")
    if client.ping():
        print("✓ Connected to Redis successfully")
    
    # Define the key to work with
    key = "queue_image"
    
    # Check if key exists
    if not client.key_exists(key):
        print(f"Key '{key}' does not exist")
        return
    
    # Get key type
    key_type = client.get_key_type(key)
    print(f"\ntype({key}) = {key_type}")
    
    # Handle different key types
    if key_type == "string":
        value = client.string.get(key)
        print(f"GET -> {value}")
    
    elif key_type == "list":
        # Get list length first
        length = client.list.llen(key)
        print(f"List length: {length}")
        
        # Pop item from left
        item = client.list.lpop(key)
        print(f"LPOP -> {item}")
        
        # Show remaining items (optional)
        remaining = client.list.lrange(key, 0, -1)
        print(f"Remaining items: {remaining}")
    
    elif key_type == "hash":
        hash_data = client.hash.hgetall(key)
        print(f"HGETALL -> {hash_data}")
    
    elif key_type == "set":
        set_members = client.set.smembers(key)
        print(f"SMEMBERS -> {set_members}")
    
    else:
        print(f"Unsupported key type for {key}: {key_type}")
    
    # Close connection
    client.close()
    print("\n✓ Connection closed")


def example_with_context_manager():
    """Example using context manager for automatic connection handling"""
    
    with RedisClient.from_env(".env") as client:
        key = "queue_image"
        
        if client.key_exists(key):
            key_type = client.get_key_type(key)
            print(f"Key type: {key_type}")
            
            if key_type == "list":
                item = client.list.lpop(key)
                print(f"Popped item: {item}")


def example_list_operations():
    """Example demonstrating list operations"""
    
    with RedisClient.from_env(".env") as client:
        key = "my_queue"
        
        # Push items to the list
        client.list.rpush(key, "item1", "item2", "item3")
        print(f"Pushed 3 items to {key}")
        
        # Get all items
        items = client.list.lrange(key, 0, -1)
        print(f"All items: {items}")
        
        # Pop from left
        item = client.list.lpop(key)
        print(f"Popped: {item}")
        
        # Get remaining items
        remaining = client.list.lrange(key, 0, -1)
        print(f"Remaining: {remaining}")


if __name__ == "__main__":
    main()
    
    # Uncomment to run other examples
    print("\n" + "="*50)
    example_with_context_manager()
    print("\n" + "="*50)
    example_list_operations()
