#!/usr/bin/env python3
"""
Hardened policy shields and reward shaping for claim negotiation.

Shields are enforced either by:
- Constraining the outcome space / issues (mechanism level)
- Masking illegal actions inside the negotiator
- Penalizing violations in the reward / utility function
"""

from typing import Dict, Tuple, Any
import numpy as np

ISSUE_BOUNDS = {
    "allowed_pct": (50, 120),
    "prompt_pay_discount": (0, 25),
    "evidence_strength": (0, 100),
    "escalate_to_imr": (0, 1),
}

def is_legal_offer(offer: Dict[str, Any]) -> bool:
    for k, (lo, hi) in ISSUE_BOUNDS.items():
        if k in offer and not (lo <= offer[k] <= hi):
            return False
    return True

def shield_penalty(offer: Dict[str, Any]) -> float:
    """Negative reward for any out-of-bound proposal."""
    pen = 0.0
    for k, (lo, hi) in ISSUE_BOUNDS.items():
        if k in offer:
            v = offer[k]
            if v < lo or v > hi:
                pen -= 0.5
    if offer.get("escalate_to_imr") == 1 and offer.get("evidence_strength", 0) < 40:
        pen -= 0.3  # premature escalation penalty
    return pen

def shaped_provider_reward(
    agreement: Dict[str, Any],
    billed: float,
    steps_used: int,
    max_steps: int,
    overturn_prior: float,
) -> float:
    """Process + outcome reward for the Provider agent."""
    if not agreement:
        return -0.2 + shield_penalty({})
    pct = agreement.get("allowed_pct", 50)
    disc = agreement.get("prompt_pay_discount", 0)
    recovery_frac = (pct / 100.0) * (1 - disc / 100.0)
    efficiency = 1.0 - (steps_used / max(max_steps, 1))
    evidence_bonus = agreement.get("evidence_strength", 0) / 100.0 * 0.1
    escalate_pen = -0.15 if agreement.get("escalate_to_imr") == 1 else 0.0
    base = recovery_frac * 0.6 + efficiency * 0.2 + evidence_bonus + escalate_pen
    return base + shield_penalty(agreement) + overturn_prior * 0.05

def shaped_payer_reward(
    agreement: Dict[str, Any],
    billed: float,
    steps_used: int,
    max_steps: int,
) -> float:
    """Process + outcome reward for the Payer agent."""
    if not agreement:
        return 0.1 + shield_penalty({})
    pct = agreement.get("allowed_pct", 50)
    disc = agreement.get("prompt_pay_discount", 0)
    cost_frac = (pct / 100.0) * (1 - disc / 100.0)
    efficiency = 1.0 - (steps_used / max(max_steps, 1))
    escalate_pen = -0.25 if agreement.get("escalate_to_imr") == 1 else 0.0
    base = (1.0 - cost_frac) * 0.55 + efficiency * 0.15 + escalate_pen
    return base + shield_penalty(agreement)

def apply_shields_to_offer(offer: Dict[str, Any]) -> Dict[str, Any]:
    """Project an offer back into the legal set (hard shield)."""
    out = dict(offer)
    for k, (lo, hi) in ISSUE_BOUNDS.items():
        if k in out:
            out[k] = int(np.clip(out[k], lo, hi))
    return out
