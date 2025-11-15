# FastAPI Opinionated EventBus Extension

FastAPI Opinionated EventBus is an optional extension for the FastAPI Opinionated Core framework that provides internal event handling capabilities for decoupled communication between components within your FastAPI applications.

## Overview

This package extends the FastAPI Opinionated Core framework by adding internal event bus functionality through a plugin system. It allows you to easily implement decoupled communication patterns within your application using events and handlers, without relying on external message queues or services.

## Features

- **Internal Event System**: Provides event emission and handling capabilities for internal application communication
- **Plugin Architecture**: Integrates seamlessly with the FastAPI Opinionated Core plugin system
- **Async/Sync Handler Support**: Supports both asynchronous and synchronous event handlers with automatic execution context management
- **Convenience Accessor**: Provides easy access to the event bus API for emitting events and registering handlers
- **Decorator-Based Registration**: Use `@OnInternalEvent` decorator to register event handlers
- **Lifecycle Management**: Properly handles event handler cleanup on application shutdown
- **Exception Handling**: Robust error handling with detailed error messages and stack traces
- **Logging Integration**: Comprehensive logging with namespace support and event tracking

## Installation

```bash
# Install via Poetry (recommended)
poetry add fastapi-opinionated-eventbus

# Or via pip
pip install fastapi-opinionated-eventbus
```

## Quick Start

### 1. Enable the EventBus plugin

```python
from fastapi_opinionated import App
from fastapi_opinionated_eventbus import EventBusPlugin

# Configure the plugin before creating the app
App.configurePlugin(EventBusPlugin())

# Create your application
app = App.create(title="My API with EventBus")
```

### 2. Register event handlers

```python
from fastapi_opinionated_eventbus import OnInternalEvent

@OnInternalEvent("user.created")
async def handle_user_created(user_data: dict):
    print(f"Handling user creation: {user_data}")
    # Could send welcome email, update analytics, etc.

@OnInternalEvent("user.updated")
def handle_user_updated(user_data: dict):
    print(f"Handling user update: {user_data}")
    # Could update cache, log changes, etc.
```

### 3. Emit events from your application

```python
from fastapi_opinionated_eventbus import eventbus_api

# In your route handler or service
@app.post("/users")
async def create_user(user: dict):
    # Create user logic here
    user_data = {"id": 1, "name": "Jane Doe", **user}

    # Emit event to notify other parts of the application
    await eventbus_api().emit("user.created", user_data)

    return user_data
```

## Configuration

The EventBus plugin can be configured with the following options:

```python
from fastapi_opinionated import App
from fastapi_opinionated_eventbus import EventBusPlugin

# Configure the plugin with custom options (currently no required config)
App.configurePlugin(EventBusPlugin())
app = App.create()
```

## Advanced Usage

### Multiple Handlers for the Same Event

You can register multiple handlers for the same event - they will all be executed:

```python
@OnInternalEvent("order.completed")
async def send_email_notification(order_data: dict):
    # Send email notification asynchronously
    pass

@OnInternalEvent("order.completed")
def update_inventory(order_data: dict):
    # Update inventory synchronously
    pass

@OnInternalEvent("order.completed")
async def log_order_completion(order_data: dict):
    # Log the order completion
    pass
```

### Passing Multiple Arguments

Event handlers can accept multiple arguments:

```python
@OnInternalEvent("payment.processed")
async def handle_payment_result(payment_id: str, status: str, amount: float):
    print(f"Payment {payment_id} has status {status} for amount {amount}")

# Emit with multiple arguments
await eventbus_api().emit("payment.processed", "payment_123", "success", 99.99)
```

### Error Handling

The EventBus plugin provides comprehensive error handling:

```python
@OnInternalEvent("critical.event")
async def critical_handler(data: dict):
    # If this handler fails, other handlers will still execute
    # Error will be logged with detailed traceback
    pass
```

## Architecture

The package consists of:

- **EventBusPlugin**: A plugin class that extends BasePlugin and handles the initialization and event management within the plugin lifecycle
- **eventbus_api()**: A helper function that provides access to the event bus instance from the application's plugin registry
- **OnInternalEvent**: A decorator for registering event handlers that automatically connects them to the event system using PluginRegistryStore
- **_EventBus**: Internal event bus implementation that manages event emission and handler execution
- **Integration**: Seamlessly integrates with the FastAPI Opinionated Core plugin system and lifecycle management

### Plugin Lifecycle Integration

The EventBus plugin properly handles lifecycle management through multiple lifecycle hooks:

- `on_controllers_loaded`: Collects all registered event handlers from the registry after controller discovery
- `on_shutdown`: Clears all registered event handlers to prevent memory leaks

## Best Practices

1. **Use Descriptive Event Names**: Use clear, descriptive event names following a consistent convention (e.g., `entity.action` like `user.created`, `order.completed`)
2. **Handle Errors Gracefully**: Event handlers should be resilient to errors as they may affect the overall application behavior
3. **Avoid Heavy Operations**: Keep event handlers lightweight; consider using background tasks for heavy operations
4. **Use Async When Possible**: Use async handlers for I/O-bound operations to maintain application performance
5. **Group Related Logic**: Group related event handling logic in the same domain folder for better organization

## CLI Integration

The EventBus plugin can be managed using the FastAPI Opinionated CLI:

```bash
# Enable the EventBus plugin
fastapi-opinionated plugins enable fastapi_opinionated_eventbus.plugin.EventBusPlugin

# List registered event handlers
fastapi-opinionated list plugins --plugin eventbus

# List all application routes
fastapi-opinionated list routes
```

## Troubleshooting

### Common Issues

1. **Plugin Not Enabled**: Make sure to enable the EventBusPlugin before using event handlers
2. **Circular Dependencies**: Avoid circular dependencies between event handlers
3. **Event Handler Not Triggering**: Verify that App.configurePlugin() is called before App.create()

### Debugging

Enable verbose logging to debug event handling:

```python
from fastapi_opinionated.shared.logger import ns_logger
logger = ns_logger("EventBus")
```

## Note

FastAPI Opinionated EventBus is an **optional extension** of the FastAPI Opinionated Core framework. It provides additional functionality for applications that require internal event-driven communication patterns, but is not required for basic FastAPI Opinionated Core functionality.