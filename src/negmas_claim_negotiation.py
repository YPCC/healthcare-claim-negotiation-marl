#!/usr/bin/env python3
"""
NegMAS SAO (Stacked Alternating Offers) scenario for healthcare claim negotiation.

Provider vs Payer with issues:
  - allowed_pct
  - prompt_pay_discount
  - evidence_strength
  - escalate_to_imr

Can be extended with negmas-llm or negmas-rl-tutorial.
"""

from negmas import SAOMechanism, AspirationNegotiator, TimeBasedConcedingNegotiator
from negmas.outcomes import make_issue
from negmas.preferences import LinearAdditiveUtilityFunction

def create_claim_session(n_steps=8, seed_context=None):
    issues = [
        make_issue(name="allowed_pct", values=(50, 120)),
        make_issue(name="prompt_pay_discount", values=(0, 25)),
        make_issue(name="evidence_strength", values=(0, 100)),
        make_issue(name="escalate_to_imr", values=(0, 1)),
    ]

    provider_ufun = LinearAdditiveUtilityFunction(
        values={
            "allowed_pct": lambda x: (x - 50) / 70.0,
            "prompt_pay_discount": lambda x: 1.0 - (x / 25.0),
            "evidence_strength": lambda x: x / 100.0,
            "escalate_to_imr": lambda x: 0.4 if x == 0 else 0.0,
        },
        weights={"allowed_pct": 0.50, "prompt_pay_discount": 0.15,
                 "evidence_strength": 0.25, "escalate_to_imr": 0.10},
        reserved_value=0.22,
        name="Provider",
    )

    payer_ufun = LinearAdditiveUtilityFunction(
        values={
            "allowed_pct": lambda x: 1.0 - ((x - 50) / 70.0),
            "prompt_pay_discount": lambda x: x / 25.0,
            "evidence_strength": lambda x: 1.0 - (x / 100.0),
            "escalate_to_imr": lambda x: 0.7 if x == 0 else 0.15,
        },
        weights={"allowed_pct": 0.48, "prompt_pay_discount": 0.18,
                 "evidence_strength": 0.14, "escalate_to_imr": 0.20},
        reserved_value=0.18,
        name="Payer",
    )

    session = SAOMechanism(issues=issues, n_steps=n_steps, name="ClaimNegotiation")

    provider = AspirationNegotiator(name="Provider_Billing", aspiration_type="boulware")
    payer = TimeBasedConcedingNegotiator(name="Payer_Adjuster")

    session.add(provider, ufun=provider_ufun)
    session.add(payer, ufun=payer_ufun)

    return session, seed_context or {}

def run_and_report(session, context):
    print(f"\n=== Running: {context.get('id', 'generic')} ===")
    if context:
        print(f"Treatment: {context.get('treatment')}")
        print(f"Prior overturn prob: {context.get('overturn_probability')}")

    state = session.run()

    print(f"Agreement: {state.agreement}")
    print(f"Steps: {state.step} | Broken: {state.broken} | Timed out: {state.timedout}")

    if state.agreement:
        names = [i.name for i in session.issues]
        agreement = dict(zip(names, state.agreement))
        print("Final terms:", agreement)
        if context.get("billed_amount"):
            pct = agreement.get("allowed_pct", 0)
            disc = agreement.get("prompt_pay_discount", 0)
            recovered = context["billed_amount"] * (pct / 100.0) * (1 - disc / 100.0)
            print(f"Estimated recovery: ${recovered:,.0f}")
    else:
        print("No agreement — would proceed to IMR or remain denied.")

    return state

if __name__ == "__main__":
    session, ctx = create_claim_session(n_steps=8)
    run_and_report(session, {"id": "demo", "treatment": "Generic claim", "billed_amount": 5000})
