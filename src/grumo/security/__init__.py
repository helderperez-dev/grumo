"""Grumo security package.

This package re-exports the names that previously lived in the flat
``grumo/security.py`` module, now split by concern:

- ``grumo/security/headers.py`` — ``SecurityHeadersMiddleware``
- ``grumo/security/cors.py`` — ``CORSMiddleware``
- ``grumo/security/csrf.py`` — ``CSRFMiddleware``, ``generate_csrf_token``,
  ``set_csrf_cookie``
- ``grumo/security/rate_limit.py`` — ``RateLimiter``, ``RateLimitMiddleware``
  and the shared ``rate_limiter`` singleton
- ``grumo/security/passwords.py`` — ``validate_password_strength``
- ``grumo/security/secrets.py`` — ``SecretStore``, ``EnvSecretStore``,
  ``LocalSecretStore``, ``secrets``, ``configure`` (Sprint 19)
- ``grumo/security/redaction.py`` — ``redact``, ``redact_string``,
  ``RedactionGuard`` (Sprint 19)
"""

from grumo.security.cors import CORSMiddleware
from grumo.security.csrf import (
    CSRFMiddleware,
    generate_csrf_token,
    set_csrf_cookie,
)
from grumo.security.headers import SecurityHeadersMiddleware
from grumo.security.passwords import validate_password_strength
from grumo.security.rate_limit import (
    RateLimiter,
    RateLimitMiddleware,
    rate_limiter,
)
from grumo.security.redaction import RedactionGuard, redact, redact_string
from grumo.security.secrets import (
    EnvSecretStore,
    LocalSecretStore,
    SecretsError,
    SecretStore,
    secrets,
)
from grumo.security.secrets import (
    configure as configure_secrets,
)

__all__ = [
    # Headers
    "SecurityHeadersMiddleware",
    # CORS
    "CORSMiddleware",
    # CSRF
    "CSRFMiddleware",
    "generate_csrf_token",
    "set_csrf_cookie",
    # Rate limiting
    "RateLimiter",
    "RateLimitMiddleware",
    "rate_limiter",
    # Passwords
    "validate_password_strength",
    # Secrets (Sprint 19)
    "SecretStore",
    "EnvSecretStore",
    "LocalSecretStore",
    "SecretsError",
    "secrets",
    "configure_secrets",
    # Redaction (Sprint 19)
    "RedactionGuard",
    "redact",
    "redact_string",
]
