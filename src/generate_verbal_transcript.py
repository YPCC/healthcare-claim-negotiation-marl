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
        for step, offer in enumerate(session.history, 1):
            if offer and hasattr(offer, "offer") and offer.offer:
                hist_offer = dict(zip(names, offer.offer))
                history.append({"step": step, "agent": str(offer.negotiator), "offer": hist_offer})

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
    findings = seed.get("findings_summary", "")[:200]
    billed = seed.get("billed_amount", 0)

    if role.lower().startswith("provider"):
        if is_final and not esc:
            return (f"Provider Billing Specialist: Given the clinical record — {findings} — "
                    f"we accept the package of {pct}% of billed (${billed * pct/100 * (1-disc/100):,.0f} estimated recovery) "
                    f"with a {disc}% prompt-pay discount and evidence credit of {evid}. No escalation to IMR. We can close this today.")
        return (f"Provider Billing Specialist: Based on the Findings ({findings}), "
                f"we are proposing {pct}% allowed, {disc}% prompt-pay, and evidence strength of {evid}. "
                f"{'We are prepared to escalate if needed.' if esc else 'We prefer to settle inside the system.'}")
    else:
        return (f"Payer Adjuster: Our counter is {pct}% of billed with a {disc}% prompt-pay discount. "
                f"Evidence strength noted at {evid}. {'We will allow escalation review.' if esc else 'We believe this stays within policy and can be closed without external review.'}")

def generate_transcript(result: Dict[str, Any]) -> str:
    seed = result["seed"]
    lines = [
        f"=== Claim Negotiation Transcript ===",
        f"Reference: {seed.get('reference_style', seed.get('id', 'N/A'))}",
        f"Treatment: {seed.get('treatment')} | Billed: ${seed.get('billed_amount')}",
        f"Findings: {seed.get('findings_summary')}",
        f"Overturn prior: {seed.get('overturn_probability')}",
        "",
        "--- Dialogue ---",
    ]
    history = result.get("history") or []
    for h in history:
        role = "Provider" if "Provider" in str(h["agent"]) else "Payer"
        lines.append(offer_to_speech(role, h["offer"], seed, h["step"]))
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
