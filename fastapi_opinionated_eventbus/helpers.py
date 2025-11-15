#fastapi-opinionated-eventbus/fastapi_opinionated_eventbus/helpers.py
import asyncio
import traceback
import inspect
from fastapi_opinionated.shared.logger import ns_logger
from fastapi_opinionated.exceptions.plugin_exception import PluginException
from fastapi_opinionated.app import App
from fastapi_opinionated.registry.plugin_store import PluginRegistryStore
from fastapi_opinionated.registry.plugin import PluginRegistry
logger = ns_logger("EventBus")



class _EventBus:
    @staticmethod
    async def emit(event_name: str, /, *args, **kwargs):
        from fastapi_opinionated_eventbus.plugin import EventBusPlugin
        
        try:
            handlers = EventBusPlugin._handlers
            tasks = []
            for handler in handlers:
                # jika async → await
                if inspect.iscoroutinefunction(handler):
                    tasks.append(handler(*args, **kwargs))
                else:
                    # jika sync, jalanin di event loop
                    tasks.append(asyncio.to_thread(handler, *args, **kwargs))

            if tasks:
                logger.info(f"Emitting event '{event_name}' to {len(tasks)} handlers.")
                await asyncio.gather(*tasks)
        except Exception as e:
            traceback.print_exc()
            raise PluginException("EventBusPlugin", f"Error emitting event '{event_name}': {e}") from e
        
def eventbus_api()->_EventBus:
    PluginRegistry.ensure_enabled("eventbus")
    return App.plugin.eventbus

def OnInternalEvent(event_name: str):
    from fastapi_opinionated_eventbus.plugin import EventBusPlugin
    def wrapper(func):
        PluginRegistryStore.add(EventBusPlugin.public_name, "internal_event_handlers", {
            "event": event_name,
            "handler": func,
        })
        return func
    return wrapper
    