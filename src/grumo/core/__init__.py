"""Grumo core runtime: application object, factory, error hierarchy.

Reactive state/events and page routing are re-exported here for backwards
compatibility; their implementations live in ``grumo.ui`` and
``grumo.routing`` respectively.
"""

from grumo.core.app import App, ObservationHandle, app, create_app
from grumo.core.errors import (
    AgentError,
    AuthError,
    ComponentError,
    ConfigurationError,
    DataError,
    EventError,
    MCPError,
    MeshError,
    RoutingError,
    StateError,
    ToolError,
    GrumoError,
)
from grumo.routing.pages import PageRegistry, call_page, page, page_registry
from grumo.ui.events import (
    WebSocketManager,
    event,
    event_handlers,
    register_event,
    websocket_endpoint,
    ws_manager,
)
from grumo.ui.rendering import render_page
from grumo.ui.state import State, StateRenderer, state, state_renderer

__all__ = [
    "App",
    "ObservationHandle",
    "app",
    "create_app",
    "WebSocketManager",
    "event",
    "event_handlers",
    "register_event",
    "websocket_endpoint",
    "ws_manager",
    "render_page",
    "PageRegistry",
    "call_page",
    "page",
    "page_registry",
    "State",
    "StateRenderer",
    "state",
    "state_renderer",
    "GrumoError",
    "ConfigurationError",
    "RoutingError",
    "ComponentError",
    "StateError",
    "EventError",
    "MeshError",
    "MCPError",
    "DataError",
    "AuthError",
    "AgentError",
    "ToolError",
]
