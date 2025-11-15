# FastAPI Opinionated EventBus Extension

FastAPI Opinionated EventBus is an optional extension for the FastAPI Opinionated Core framework that provides internal event handling capabilities for decoupled communication between components within your FastAPI applications.

## Overview

This package extends the FastAPI Opinionated Core framework by adding internal event bus functionality through a plugin system. It allows you to easily implement decoupled communication patterns within your application using events and handlers, without relying on external message queues or services.

## Features

- **Internal Event System**: Provides event emission and handling capabilities for internal application communication
- **Plugin Architecture**: Integrates seamlessly with the FastAPI Opinionated Core plugin system
- **Async/Sync Handler Support**: Supports both asynchronous and synchronous event handlers
- **Convenience Accessor**: Provides easy access to the event bus API for emitting events and registering handlers
- **Decorator-Based Registration**: Use `@OnInternalEvent` decorator to register event handlers
- **Lifecycle Management**: Properly handles event handler cleanup on application shutdown

## Installation

```bash
# Install via Poetry (recommended)
poetry add fastapi-opinionated-eventbus

# Or via pip
pip install fastapi-opinionated-eventbus
```

## Usage

### Configuration

First, enable the EventBus plugin in your application:

```python
from fastapi_opinionated import App
from fastapi_opinionated_eventbus import EventBusPlugin

app = App.create()  # FastAPI Factory

# Enable the EventBus plugin
App.enable(EventBusPlugin())
```

### Registering Event Handlers

Use the `@OnInternalEvent` decorator to register event handlers:

```python
from fastapi_opinionated_eventbus import OnInternalEvent

@OnInternalEvent("user.created")
async def handle_user_created(user_data: dict):
    print(f"User created: {user_data}")
    # Perform async operations like sending emails, updating caches, etc.

@OnInternalEvent("order.completed")
def handle_order_completed(order_data: dict):
    print(f"Order completed: {order_data}")
    # Perform sync operations
```

### Emitting Events

Use the event bus API to emit events:

```python
from fastapi_opinionated_eventbus import eventbus_api

# Emit an event with data
await eventbus_api().emit("user.created", {"id": 1, "name": "John Doe"})
```

### Complete Example

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_opinionated import App
from fastapi_opinionated_eventbus import EventBusPlugin, OnInternalEvent, eventbus_api

# Register event handlers
@OnInternalEvent("user.created")
async def handle_user_created(user_data: dict):
    print(f"Handling user creation: {user_data}")
    # Could send welcome email, update analytics, etc.

@OnInternalEvent("user.updated")
def handle_user_updated(user_data: dict):
    print(f"Handling user update: {user_data}")
    # Could update cache, log changes, etc.

# Create your application
app = App.create(title="My API with EventBus")

# Enable the EventBus plugin
App.enable(EventBusPlugin())

# Example endpoint that emits an event
@app.post("/users")
async def create_user(user: dict):
    # Create user logic here
    user_data = {"id": 1, "name": "John Doe", **user}
    
    # Emit event
    await eventbus_api().emit("user.created", user_data)
    
    return user_data
```

## Architecture

The package consists of:

- **EventBusPlugin**: A plugin class that extends BasePlugin and handles the initialization and event management
- **eventbus_api()**: A helper function that provides access to the event bus instance from the application's plugin registry
- **OnInternalEvent**: A decorator for registering event handlers that automatically connects them to the event system
- **InternalEventRegistry**: A registry that maintains the mapping of events to their handlers
- **Integration**: Seamlessly integrates with the FastAPI Opinionated Core plugin system and lifecycle management

## Plugin Lifecycle

The EventBus plugin properly handles lifecycle management:

- On startup: Initializes the event bus system
- On shutdown: Clears all registered event handlers to prevent memory leaks

## Note

FastAPI Opinionated EventBus is an **optional extension** of the FastAPI Opinionated Core framework. It provides additional functionality for applications that require internal event-driven communication patterns, but is not required for basic FastAPI Opinionated Core functionality.