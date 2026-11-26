"""Grumo runtime — the unified execution model.

This package makes the computational model *operational*.
Every meaningful operation is represented as an Execution produced by a
single ExecutionEngine walking the operational model:

    World → Goal → Intent → Capability → Policy → Execution → Effect → Observation
"""

from __future__ import annotations

from grumo.primitives.capability import Capability
from grumo.primitives.intent import Intent
from grumo.runtime.agency import (
    AdaptiveRun,
    AdaptiveSupervisor,
    Goal,
    GoalDecomposer,
    GoalIntentRun,
    GoalRun,
    GoalRuntime,
    GoalStatus,
    GoalStore,
    SQLiteGoalStore,
    SupervisorConfig,
    SupervisorDecision,
    GrumoStoreGoalStore,
)
from grumo.runtime.application_graph import (
    ApplicationEdge,
    ApplicationGraph,
    ApplicationGraphChange,
    ApplicationGraphContributor,
    ApplicationNode,
    ApplicationNodeKind,
    ChangeReason,
    Extension,
    ExtensionManifest,
    Invalidation,
    InvalidationEngine,
    build_application_graph,
    contribute_goal,
    diff_application_graph,
)
from grumo.runtime.capability import CapabilityResolver, Resolution
from grumo.runtime.constraint import ConstraintEnforcer, Decision, ResourceAccountant
from grumo.runtime.context import ExecutionContext, current_context, use_context
from grumo.runtime.conventions import ApplicationLayout, discover_layout
from grumo.runtime.dependency_graph import (
    DependencyGraph,
    DependencyRevision,
    DirtyNode,
)
from grumo.runtime.distributed import (
    FabricLease,
    FabricRoutingError,
    FabricWork,
    MemberStatus,
    NodeAdvertisement,
    NodeMembership,
    NoEligibleNodeError,
    PlacementDecision,
    PlacementRequirement,
    RuntimeFabric,
    GrumoStoreMembershipStore,
    WorkNotFailoverSafeError,
)
from grumo.runtime.errors import (
    AgentExecutionError,
    ApprovalRequired,
    CapabilityDenied,
    ConstraintViolation,
    ExecutionCancelled,
    ExecutionError,
    ExecutionTimeout,
    ResourceExceeded,
    ToolExecutionError,
    ValidationError,
    WorkflowFailure,
)
from grumo.runtime.execution import Execution, ExecutionStatus
from grumo.runtime.execution.engine import (
    ComputeFn,
    ComputeResult,
    ExecutionEngine,
    engine,
)
from grumo.runtime.execution.world import (
    bind_world,
    resolve_target_entity_id,
    world_aware,
)
from grumo.runtime.extension import (
    ExtensionState,
    ExtensionStatus,
    RuntimeExtensionRegistry,
)
from grumo.runtime.graph import ExecutionGraph, ExecutionNode
from grumo.runtime.human import (
    Approval,
    ApprovalRegistry,
    ApprovalStatus,
    Human,
    ask_human,
)
from grumo.runtime.identity import (
    AuthenticationEvidence,
    Identity,
    IdentityKind,
    IdentityStatus,
    Principal,
)
from grumo.runtime.identity_store import IdentityStore, GrumoStoreIdentityStore
from grumo.runtime.inspection import (
    LineageEvent,
    RuntimeLineage,
    lineage,
    runtime_dashboard,
)
from grumo.runtime.operations import OperationalRuntime
from grumo.runtime.persistence import (
    ExecutionStore,
    InMemoryExecutionStore,
    JSONFileExecutionStore,
)
from grumo.runtime.planner import ComputeParticipant, Plan, Planner, PlanStep
from grumo.runtime.policy import (
    PolicyDecision,
    PolicyEngine,
    PolicyRequest,
    PolicyResult,
    PolicyRule,
)
from grumo.runtime.reconciliation import (
    GoalIntentFactory,
    GoalPredicate,
    GoalReconciliation,
    ReconcileAction,
    ReconcileDecision,
    ReconcileGuard,
    ReconcileHandler,
    ReconcileLedger,
    Reconciler,
)
from grumo.runtime.runtime import (
    ConvergenceStatus,
    Runtime,
    RuntimeConvergence,
    RuntimeCycle,
)
from grumo.runtime.scheduling.dispatch import DispatchPlan, RuntimeDispatcher
from grumo.runtime.scheduling.handoff import ExecutionHandoff, RemoteExecutionRequired
from grumo.runtime.scheduling.work import (
    RuntimeScheduler,
    ScheduledWork,
    SchedulingDecision,
    WorkEligibility,
    scheduled_work_from_intent,
)
from grumo.runtime.store import (
    DEFAULT_STORE_PATH,
    RuntimeStore,
    StoreConfig,
    StoreHealth,
    StoreProvider,
    StoreProviderError,
    StoreProviderRegistry,
    GrumoStoreProvider,
    bind_active_runtime_store,
    create_store_provider,
    get_active_runtime_store,
    store_registry,
)
from grumo.runtime.task import Task, TaskStatus
from grumo.runtime.transaction import (
    OutboxDispatcher,
    OutboxMessage,
    RuntimeTransaction,
    dispatch_events,
    dispatch_outbox,
    transaction,
)
from grumo.runtime.workflow import Workflow, WorkflowRun, WorkflowStrategy
from grumo.runtime.workflow_store import GrumoStoreWorkflowStore, WorkflowStore

__all__ = [
    "ConvergenceStatus",
    "Runtime",
    "RuntimeConvergence",
    "RuntimeCycle",
    "ApplicationNodeKind",
    "ChangeReason",
    "Extension",
    "ExtensionManifest",
    "Invalidation",
    "InvalidationEngine",
    "ApplicationNode",
    "ApplicationEdge",
    "ApplicationGraph",
    "ApplicationGraphChange",
    "ApplicationGraphContributor",
    "build_application_graph",
    "contribute_goal",
    "diff_application_graph",
    "Execution",
    "ExecutionStatus",
    "ExtensionState",
    "ExtensionStatus",
    "RuntimeExtensionRegistry",
    "ExecutionContext",
    "current_context",
    "use_context",
    "ExecutionEngine",
    "engine",
    "ComputeFn",
    "ComputeResult",
    "CapabilityResolver",
    "Resolution",
    "PolicyDecision",
    "PolicyEngine",
    "PolicyRequest",
    "PolicyResult",
    "PolicyRule",
    "ApplicationLayout",
    "discover_layout",
    "DependencyGraph",
    "DependencyRevision",
    "DirtyNode",
    "ConstraintEnforcer",
    "Decision",
    "ResourceAccountant",
    "ExecutionError",
    "CapabilityDenied",
    "ConstraintViolation",
    "ResourceExceeded",
    "ExecutionTimeout",
    "ExecutionCancelled",
    "ToolExecutionError",
    "AgentExecutionError",
    "ValidationError",
    "ApprovalRequired",
    "WorkflowFailure",
    "IdentityKind",
    "IdentityStatus",
    "Identity",
    "AuthenticationEvidence",
    "Principal",
    "IdentityStore",
    "GrumoStoreIdentityStore",
    "MemberStatus",
    "NodeAdvertisement",
    "NodeMembership",
    "GrumoStoreMembershipStore",
    "PlacementRequirement",
    "PlacementDecision",
    "FabricWork",
    "FabricLease",
    "RuntimeFabric",
    "FabricRoutingError",
    "NoEligibleNodeError",
    "WorkNotFailoverSafeError",
    "Task",
    "TaskStatus",
    "Workflow",
    "WorkflowRun",
    "WorkflowStrategy",
    "WorkflowStore",
    "GrumoStoreWorkflowStore",
    "ExecutionGraph",
    "ExecutionNode",
    "Approval",
    "ApprovalStatus",
    "ApprovalRegistry",
    "Human",
    "ExecutionHandoff",
    "RemoteExecutionRequired",
    "LineageEvent",
    "RuntimeLineage",
    "lineage",
    "ask_human",
    "ExecutionStore",
    "InMemoryExecutionStore",
    "JSONFileExecutionStore",
    "DEFAULT_STORE_PATH",
    "StoreConfig",
    "StoreHealth",
    "StoreProvider",
    "StoreProviderError",
    "StoreProviderRegistry",
    "RuntimeStore",
    "GrumoStoreProvider",
    "bind_active_runtime_store",
    "create_store_provider",
    "get_active_runtime_store",
    "store_registry",
    "RuntimeTransaction",
    "OutboxMessage",
    "OutboxDispatcher",
    "transaction",
    "dispatch_outbox",
    "dispatch_events",
    "ComputeParticipant",
    "Plan",
    "PlanStep",
    "Planner",
    "AdaptiveRun",
    "AdaptiveSupervisor",
    "SupervisorDecision",
    "SupervisorConfig",
    "Goal",
    "GoalStatus",
    "GoalIntentRun",
    "GoalRun",
    "GoalRuntime",
    "GoalDecomposer",
    "GoalStore",
    "SQLiteGoalStore",
    "GrumoStoreGoalStore",
    "OperationalRuntime",
    "runtime_dashboard",
    "bind_world",
    "world_aware",
    "resolve_target_entity_id",
    "GoalIntentFactory",
    "GoalPredicate",
    "GoalReconciliation",
    "ReconcileAction",
    "ReconcileDecision",
    "ReconcileGuard",
    "ReconcileHandler",
    "ReconcileLedger",
    "Reconciler",
    "RuntimeScheduler",
    "ScheduledWork",
    "SchedulingDecision",
    "WorkEligibility",
    "scheduled_work_from_intent",
    "DispatchPlan",
    "RuntimeDispatcher",
    "execute",
    "register_capability",
    "grant",
]


async def execute(
    intent: Intent,
    compute: ComputeFn | None = None,
    *,
    actor: str = "system",
    principal: Principal | None = None,
    capabilities: list[str] | None = None,
    output_type: type | None = None,
    parent: ExecutionContext | None = None,
) -> Execution:
    """Execute an intent through the default runtime engine."""
    return await engine.execute(
        intent,
        compute,
        actor=actor,
        principal=principal,
        capabilities=capabilities,
        output_type=output_type,
        parent=parent,
    )


def register_capability(capability: Capability) -> None:
    """Register a capability template with the default engine."""
    engine.capabilities.register(capability)


def grant(context: ExecutionContext, capability: Capability) -> None:
    """Grant a capability to an in-flight execution context."""
    context.grant(capability)
