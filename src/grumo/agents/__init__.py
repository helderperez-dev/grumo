"""Agents — durable entity registry (Sprint 17).

Agents are compute participants with stable identity, capabilities, state,
and queryable execution history. The registry persists agent metadata and
links every run to its execution record.

    from grumo import AgentEntity, AgentRegistry, SQLiteAgentRegistry

    registry = SQLiteAgentRegistry("data/agents.db")
    entity = AgentEntity(
        agent_id="lead-scorer",
        name="Lead Scorer",
        model="openai:gpt-4o",
        capabilities=["scoring.read"],
    )
    await registry.register(entity)
    agent = Agent(model="openai:gpt-4o", agent_id="lead-scorer", registry=registry)
"""

from grumo.agents.models import AgentEntity, AgentRunRecord
from grumo.agents.registry import (
    AgentRegistry,
    InMemoryAgentRegistry,
    SQLiteAgentRegistry,
)

__all__ = [
    "AgentEntity",
    "AgentRegistry",
    "AgentRunRecord",
    "InMemoryAgentRegistry",
    "SQLiteAgentRegistry",
]
