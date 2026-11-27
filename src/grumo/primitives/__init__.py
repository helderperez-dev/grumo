"""Grumo computational model.

The fundamental ontology from which all higher-level capabilities emerge:

    Entity      — anything that holds state (conceptual; represented via State)
    State       — durable system truth
    Intent      — what the system is trying to accomplish (an outcome)
    Capability  — explicit permission to produce an effect
    Effect      — a change caused outside pure computation

The runtime mechanism is Execution; its dimensions are Compute, Time,
Resource, and Constraint. AI is one form of Compute.

These are computational concepts, not application features.

    ENTITY → STATE → INTENT → CAPABILITY → EXECUTION → EFFECT → STATE
    TIME + CONSTRAINT surround the entire lifecycle.
    RESOURCE determines how execution should be performed.

The sophistication should be in the model, not in the API surface.
"""

from grumo.primitives.capability import Capability
from grumo.primitives.compute import ComputeKind, ComputeSpec
from grumo.primitives.constraint import Constraint
from grumo.primitives.effect import Effect, EffectStatus
from grumo.primitives.intent import Intent, IntentStatus
from grumo.primitives.resource import Resource
from grumo.primitives.state import State
from grumo.primitives.time import TimeSpec

__all__ = [
    "State",
    "Capability",
    "Intent",
    "IntentStatus",
    "Effect",
    "EffectStatus",
    "TimeSpec",
    "ComputeSpec",
    "ComputeKind",
    "Resource",
    "Constraint",
]
