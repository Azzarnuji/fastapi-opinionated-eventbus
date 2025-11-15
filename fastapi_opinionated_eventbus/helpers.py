# fastapi-opinionated-eventbus/fastapi_opinionated_eventbus/helpers.py

import asyncio
import traceback
import inspect
from typing import List
from fastapi_opinionated.shared.logger import ns_logger
from fastapi_opinionated.exceptions.plugin_exception import PluginException
from fastapi_opinionated.app import App
from fastapi_opinionated.registry.plugin import PluginRegistry
from fastapi_opinionated.registry.plugin_store import PluginRegistryStore

logger = ns_logger("EventBus")


class _EventBus:
    """
    EventBus:
    - Handlers grouped by event_name
    - Supports sync + async handlers
    """

    _handlers: List[dict] = []

    # ------------------------------------------------------------------
    # REGISTER handler for a specific event
    # ------------------------------------------------------------------
    @classmethod
    def register(cls, event_name: str, handler):
        cls._handlers.setdefault(event_name, []).append(handler)
        logger.info(f"Registered handler '{handler.__name__}' for event '{event_name}'")

    # ------------------------------------------------------------------
    # EMIT EVENT
    # ------------------------------------------------------------------
    @classmethod
    async def emit(cls, event_name: str, *args, **kwargs):
        from fastapi_opinionated_eventbus.plugin import EventBusPlugin

        try:
            handlers = [h["handler"] for h in cls._handlers if h["event"] == event_name]
            logger.info(f"Type: {type(handlers)}, {handlers}")

            logger.info(f"Emitting '{event_name}' to {len(handlers)} handlers")

            if not handlers:
                return

            tasks = []

            for handler in handlers:

                if inspect.iscoroutinefunction(handler):
                    tasks.append(handler(*args, **kwargs))
                else:
                    tasks.append(asyncio.to_thread(handler, *args, **kwargs))

            await asyncio.gather(*tasks)

        except Exception as e:
            traceback.print_exc()
            raise PluginException(
                EventBusPlugin.public_name,
                f"Error emitting event '{event_name}': {e}"
            ) from e


# ----------------------------------------------------------------------
# PUBLIC API DIPAKAI CONTROLLER / SERVICE
# ----------------------------------------------------------------------
def eventbus_api() -> _EventBus:
    from fastapi_opinionated_eventbus.plugin import EventBusPlugin
    PluginRegistry.ensure_enabled(EventBusPlugin.public_name)
    return App.plugin.eventbus


# ----------------------------------------------------------------------
# DECORATOR — TETAP PAKAI PLUGIN REGISTRY STORE
# ----------------------------------------------------------------------
def OnInternalEvent(event_name: str):
    """
    Register internal event handler to PluginRegistryStore.
    The plugin will load it later and inject into _EventBus.
    """
    from fastapi_opinionated_eventbus.plugin import EventBusPlugin
    PluginRegistry.ensure_enabled(EventBusPlugin.public_name)

    def wrapper(func):
        PluginRegistryStore.add(
            EventBusPlugin.public_name,
            "internal_event_handlers",
            {
                "event": event_name,
                "handler": func,
            }
        )
        return func

    return wrapper
