"""Proofpay trust engine: pure functions, no I/O."""

from .config import DEFAULT, TrustConfig
from .events import Event
from .policy import (
    POLICIES,
    AgentDecision,
    Decision,
    Line,
    agent_limit,
    authorize_agent_spend,
    auto_capture_threshold,
    choose_policy,
    evaluate,
)
from .reputation import Reputation, confidence_weight, fit_cohort_prior, reputation

__all__ = [
    "DEFAULT", "POLICIES", "AgentDecision", "Decision", "Event", "Line", "Reputation",
    "TrustConfig", "agent_limit", "authorize_agent_spend", "auto_capture_threshold",
    "choose_policy", "confidence_weight", "evaluate", "fit_cohort_prior", "reputation",
]
