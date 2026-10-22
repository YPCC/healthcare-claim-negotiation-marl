#!/usr/bin/env python3
"""
LLM negotiators for claim negotiation using negmas-llm.

Install: pip install negmas-llm
Set OPENAI_API_KEY or use Ollama locally.

Injects real IMR Findings into the system prompt so the LLM agents
ground their offers in the public determination record.
"""

from typing import Dict, Any, Optional

try:
    from negmas_llm import OpenAINegotiator, OllamaNegotiator
except ImportError:
    OpenAINegotiator = OllamaNegotiator = None

CLAIM_SYSTEM_PROMPT = """You are a healthcare claim negotiator.
You must stay inside the defined issues: allowed_pct (50-120), prompt_pay_discount (0-25),
evidence_strength (0-100), escalate_to_imr (0 or 1).
Never propose values outside these ranges. Respect ERISA-style step limits.
Ground every argument in the clinical Findings provided.
Prefer settlement when evidence is strong; escalate only when internal negotiation fails.
"""

def build_claim_prompt(seed: Dict[str, Any]) -> str:
    return (
        CLAIM_SYSTEM_PROMPT
        + f"\n\nCase ReferenceID: {seed.get('reference_id')}"
        + f"\nDiagnosis: {seed.get('diagnosis_category')}"
        + f"\nTreatment: {seed.get('treatment_category')}"
        + f"\nIMR Type: {seed.get('imr_type')}"
        + f"\nHistorical Determination: {seed.get('imr_determination')}"
        + f"\nFindings excerpt: {seed.get('findings_summary', '')[:600]}"
        + f"\nBilled amount: ${seed.get('billed_amount')}"
    )

def create_llm_negotiator(
    role: str,
    seed: Dict[str, Any],
    ufun,
    model: str = "gpt-4o-mini",
    provider: str = "openai",
    name: Optional[str] = None,
):
    """Create an LLM negotiator with claim-specific context."""
    if OpenAINegotiator is None:
        raise RuntimeError("Install negmas-llm first: pip install negmas-llm")

    prompt = build_claim_prompt(seed)
    cls = OpenAINegotiator if provider == "openai" else OllamaNegotiator
    return cls(
        model=model,
        name=name or f"{role}_LLM",
        ufun=ufun,
        system_prompt=prompt,
    )

def run_llm_session(seed: Dict[str, Any], n_steps: int = 8):
    """Minimal example: LLM Provider vs LLM Payer on one IMR seed."""
    from negmas import SAOMechanism
    from negmas.outcomes import make_issue
    from negmas.preferences import LinearAdditiveUtilityFunction

    issues = [
        make_issue(name="allowed_pct", values=(50, 120)),
        make_issue(name="prompt_pay_discount", values=(0, 25)),
        make_issue(name="evidence_strength", values=(0, 100)),
        make_issue(name="escalate_to_imr", values=(0, 1)),
    ]
    # Simplified utilities (replace with full shaped versions from policy_shields)
    provider_ufun = LinearAdditiveUtilityFunction(
        values={"allowed_pct": lambda x: (x-50)/70, "prompt_pay_discount": lambda x: 1-x/25,
                "evidence_strength": lambda x: x/100, "escalate_to_imr": lambda x: 0.5 if x==0 else 0.1},
        weights={"allowed_pct": 0.5, "prompt_pay_discount": 0.15, "evidence_strength": 0.25, "escalate_to_imr": 0.1},
        issues=issues, reserved_value=0.2, name="Provider",
    )
    payer_ufun = LinearAdditiveUtilityFunction(
        values={"allowed_pct": lambda x: 1-(x-50)/70, "prompt_pay_discount": lambda x: x/25,
                "evidence_strength": lambda x: 1-x/100, "escalate_to_imr": lambda x: 0.7 if x==0 else 0.2},
        weights={"allowed_pct": 0.5, "prompt_pay_discount": 0.2, "evidence_strength": 0.15, "escalate_to_imr": 0.15},
        issues=issues, reserved_value=0.15, name="Payer",
    )

    session = SAOMechanism(issues=issues, n_steps=n_steps)
    session.add(create_llm_negotiator("Provider", seed, provider_ufun, name="Provider_LLM"))
    session.add(create_llm_negotiator("Payer", seed, payer_ufun, name="Payer_LLM"))
    return session.run()

if __name__ == "__main__":
    print("LLM negotiator scaffolding ready. Set API key and call run_llm_session(seed).")
