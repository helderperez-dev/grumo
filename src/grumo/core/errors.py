"""Grumo error hierarchy.

Every framework error derives from `GrumoError` so applications can catch the
whole framework surface with one exception type. Subsystems may extend these
(e.g. `grumo.auth.AuthError`) without introducing new roots.
"""


class GrumoError(Exception):
    """Base class for all Grumo framework errors."""


class ConfigurationError(GrumoError):
    """Invalid or missing configuration (env vars, provider keys, options)."""


class RoutingError(GrumoError):
    """Route registration or path resolution failure."""


class ComponentError(GrumoError):
    """Component construction or rendering failure."""


class StateError(GrumoError):
    """Reactive state misuse or propagation failure."""


class EventError(GrumoError):
    """Browser/UI event handling failure."""


class MeshError(GrumoError):
    """Mesh event or remote-call failure."""


class MCPError(GrumoError):
    """MCP protocol or tool-exposure failure."""


class DataError(GrumoError):
    """Database or model operation failure."""


class AuthError(GrumoError):
    """Authentication or authorization failure."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AgentError(GrumoError):
    """Agent execution failure."""


class ToolError(GrumoError):
    """Tool registration or execution failure."""
