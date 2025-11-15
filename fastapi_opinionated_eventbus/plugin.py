#fastapi-opinionated-eventbus/fastapi_opinionated_eventbus/plugin.py
from fastapi_opinionated.app import AppCmd
from fastapi_opinionated.shared.base_plugin import BasePlugin
from fastapi_opinionated_eventbus.helpers import _EventBus
from fastapi_opinionated.shared.logger import ns_logger
from fastapi_opinionated.exceptions.plugin_exception import PluginException
from fastapi_opinionated.registry.plugin_store import PluginRegistryStore
logger = ns_logger("EventBusPlugin")
class EventBusPlugin(BasePlugin):
    public_name: str = "eventbus"
    command_name: str = "eventbus.enable"
    target_class = _EventBus
    _handlers = {}
    
    @staticmethod
    @AppCmd("eventbus.enable")
    def _internal(app, fastapi_app, *args, **kwargs):
        try:
            logger.info("Enabling EventBusPlugin")
            event = _EventBus()
            logger.info("EventBusPlugin enabled successfully")
            return event
        except Exception as e:
            raise PluginException("EventBusPlugin", cause=e)
        
    def on_controllers_loaded(self, app, fastapi_app):
        self._handlers = PluginRegistryStore.get(self.public_name).get("internal_event_handlers", [])
        for h in self._handlers:
            logger.info(f"Registered handler for event '{h['event']}'")

    def on_ready(self, app, fastapi_app, plugin_api):
        pass
    
    def on_shutdown(self, app, fastapi_app, plugin_api):
        self._handlers.clear()


