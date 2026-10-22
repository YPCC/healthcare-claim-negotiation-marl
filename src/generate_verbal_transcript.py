#!/usr/bin/env python3
"""
Generate full multi-turn verbal (natural language) transcripts for claim negotiations.

Runs a NegMAS SAO session on an IMR seed, then converts the structured offer history
into a realistic Provider ↔ Payer dialogue grounded in the Findings and negotiated numbers.

When negmas-llm is available and an API key is set, the same session can use real LLM negotiators.
This script provides a high-quality template-based fallback that produces ready-to-use transcripts.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from negmas import SAOMechanism, AspirationNegotiator, TimeBasedConcedingNegotiator
from negmas.outcomes import make_issue
from negmas.preferences import LinearAdditiveUtilityFunction

def run_structured_session(seed: Dict[str, Any], n_steps: int = 10) -> Dict[str, Any]:
    issues = [
        make_issue(name="allowed_pct", values=(50, 120)),
        make_issue(name="prompt_pay_discount", values=(0, 25)),
        make_issue(name="evidence_strength", values=(0, 100)),
        make_issue(name="escalate_to_imr", values=(0, 1)),
    ]
    provider_ufun = LinearAdditiveUtilityFunction(
        values={"allowed_pct": lambda x: (x-50)/70, "prompt_pay_discount": lambda x: 1-x/25,
                "evidence_strength": lambda x: x/100, "escalate_to_imr": lambda x: 0.4 if x==0 else 0.0},
        weights={"allowed_pct": 0.5, "prompt_pay_discount": 0.15, "evidence_strength": 0.25, "escalate_to_imr": 0.1},
        issues=issues, reserved_value=0.22, name="Provider"
    )
    payer_ufun = LinearAdditiveUtilityFunction(
        values={"allowed_pct": lambda x: 1-(x-50)/70, "prompt_pay_discount": lambda x: x/25,
                "evidence_strength": lambda x: 1-x/100, "escalate_to_imr": lambda x: 0.7 if x==0 else 0.15},
        weights={"allowed_pct": 0.48, "prompt_pay_discount": 0.18, "evidence_strength": 0.14, "escalate_to_imr": 0.2},
        issues=issues, reserved_value=0.18, name="Payer"
    )
    session = SAOMechanism(issues=issues, n_steps=n_steps)
    session.add(AspirationNegotiator(name="Provider_Billing", aspiration_type="boulware"), ufun=provider_ufun)
    session.add(TimeBasedConcedingNegotiator(name="Payer_Adjuster"), ufun=payer_ufun)
    state = session.run()

    names = [i.name for i in session.issues]
    agreement = dict(zip(names, state.agreement)) if state.agreement else None
    history = []
    if hasattr(session, "history"):
        for step_state in session.history:
            if hasattr(step_state, "new_offers") and step_state.new_offers:
                for negotiator_id, offer_tuple in step_state.new_offers:
                    if offer_tuple:
                        offer = dict(zip(names, offer_tuple))
                        role = "Provider" if "Provider" in negotiator_id else "Payer"
                        history.append({
                            "step": step_state.step,
                            "agent": role,
                            "offer": offer,
                        })

    return {
        "agreement": agreement,
        "steps": state.step,
        "broken": state.broken,
        "timedout": state.timedout,
        "history": history,
        "seed": seed,
    }

def offer_to_speech(role: str, offer: Dict[str, Any], seed: Dict[str, Any], step: int, is_final: bool = False) -> str:
    pct = offer.get("allowed_pct", 50)
    disc = offer.get("prompt_pay_discount", 0)
    evid = offer.get("evidence_strength", 0)
    esc = offer.get("escalate_to_imr", 0)
    findings = seed.get("findings_summary", "")[:220]
    billed = seed.get("billed_amount", 0)
    recovery = billed * (pct / 100.0) * (1 - disc / 100.0)

    if role == "Provider":
        if is_final:
            return (f"Provider Billing Specialist: Based on the clinical Findings — {findings} — "
                    f"we accept {pct}% of billed (estimated recovery ${recovery:,.0f}) with a {disc}% prompt-pay discount "
                    f"and evidence strength of {evid}. {'Escalation noted.' if esc else 'No escalation to IMR. Case closed.'}")
        return (f"Provider Billing Specialist (step {step}): Citing the Findings ({findings}), "
                f"we propose {pct}% allowed (${recovery:,.0f}), {disc}% prompt-pay, evidence credit {evid}. "
                f"{'Ready to escalate if no progress.' if esc else 'Prefer internal settlement.'}")
    else:
        return (f"Payer Adjuster (step {step}): Counter-offer is {pct}% of billed with {disc}% prompt-pay discount. "
                f"Evidence noted at {evid}. {'Escalation path remains open.' if esc else 'We can close within policy without external review.'}")

def generate_transcript(result: Dict[str, Any]) -> str:
    seed = result["seed"]
    lines = [
        "=== Claim Negotiation Transcript ===",
        f"Reference: {seed.get('reference_style', seed.get('id', 'N/A'))}",
        f"Treatment: {seed.get('treatment')} | Billed: ${seed.get('billed_amount')}",
        f"Findings: {seed.get('findings_summary')}",
        f"Overturn prior: {seed.get('overturn_probability')}",
        "",
        "--- Multi-turn Dialogue ---",
    ]
    history = result.get("history") or []
    for h in history:
        lines.append(offer_to_speech(h["agent"], h["offer"], seed, h["step"]))
        lines.append("")
    if result["agreement"]:
        lines.append("--- Final Agreement ---")
        lines.append(offer_to_speech("Provider", result["agreement"], seed, result["steps"], is_final=True))
        pct = result["agreement"].get("allowed_pct", 0)
        disc = result["agreement"].get("prompt_pay_discount", 0)
        rec = seed.get("billed_amount", 0) * (pct/100) * (1 - disc/100)
        lines.append(f"Estimated recovery: ${rec:,.0f} | Escalated: {bool(result['agreement'].get('escalate_to_imr'))}")
    else:
        lines.append("No agreement reached. Case would proceed to IMR or remain denied.")
    return "\n".join(lines)

def main(seed_path: str = "data/imr_example_seeds.json", seed_id: str = "seed_omnitrope_ghd", out: str = "examples/omnitrope_verbal_transcript.txt"):
    seeds = json.loads(Path(seed_path).read_text())
    seed = next((s for s in seeds if s.get("id") == seed_id), seeds[0])
    result = run_structured_session(seed)
    transcript = generate_transcript(result)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(transcript)
    print(transcript)
    print(f"\nSaved to {out}")

if __name__ == "__main__":
    main()
