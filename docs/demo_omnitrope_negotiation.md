# Demo: Omnitrope / Growth Hormone Deficiency Claim Negotiation

**Captured NegMAS SAO simulation** — Provider Billing Specialist vs Payer Adjuster  
Grounded in public DMHC IMR Findings style (medical necessity, growth hormone continuation).

## Simulation Output

```
======================================================================
NEGOTIATION SIMULATION: Omnitrope / Growth Hormone Deficiency Claim
======================================================================
Treatment: Omnitrope (growth hormone)
Diagnosis: Growth hormone deficiency + idiopathic short stature
Key evidence: Failed stimulation test, low growth velocity, prior response
Billed amount: $4,800
Historical overturn prior (IMR-style): 0.65
Max steps (appeal loops): 12
----------------------------------------------------------------------

=== RESULT ===
Agreement reached: True
Steps used: 10
Broken: False
Timed out: False

Final Agreement Terms:
  allowed_pct: 52
  prompt_pay_discount: 4
  evidence_strength: 41
  escalate_to_imr: 0

Estimated recovery: $2,396
Escalated to IMR: No

=== STEP-BY-STEP OFFER HISTORY ===
Step 1: Payer_Adjuster → (50, 25, 0, 0)
Step 2: Payer_Adjuster → (50, 25, 0, 0)
Step 3: Payer_Adjuster → (50, 25, 1, 0)
Step 4: Payer_Adjuster → (50, 25, 5, 0)
Step 5: Payer_Adjuster → (52, 25, 4, 0)
Step 6: Payer_Adjuster → (50, 22, 10, 0)
Step 7: Payer_Adjuster → (52, 23, 29, 0)
Step 8: Payer_Adjuster → (58, 25, 48, 0)
Step 9: Payer_Adjuster → (62, 18, 43, 0)
Step 10: Provider_Billing_Specialist → (52, 4, 41, 0)
======================================================================
```

Agreement tuple order: `(allowed_pct, prompt_pay_discount, evidence_strength, escalate_to_imr)`.

---

## Two-Minute Story: Agents Negotiating Under Policy and Reward

A provider billing specialist and an insurance adjuster sit across a virtual table. Between them is a claim for Omnitrope — growth hormone therapy for a young patient with documented growth hormone deficiency and idiopathic short stature. The clinical record is strong: failed stimulation test, persistently low growth velocity, and prior therapeutic response. Historical Independent Medical Review data for similar cases suggest roughly a 65% chance the denial would be overturned if the case reached external review.

Neither agent is free to do whatever it wants. Their utility functions encode competing objectives. The provider is rewarded for higher recovery percentages, recognition of clinical evidence, and avoiding costly escalation when a reasonable settlement is available. The payer is rewarded for keeping payouts lower, extracting modest prompt-pay concessions, and staying inside policy bounds. Both face reserved values — walk-away thresholds below which no deal is better than continuing the dispute.

Policy shields operate quietly in the background. The agents cannot invent offers outside the defined issue ranges. Escalation to Independent Medical Review is an explicit, costly action rather than an automatic threat. Time is limited: the mechanism allows a fixed number of appeal loops, mirroring real ERISA and internal-appeal windows. Offers that would violate basic reference-based or medical-necessity logic are either masked or heavily penalized by the utility design.

The negotiation unfolds over ten steps. Early on the payer holds near its floor — low allowed percentage, high prompt-pay discount, minimal credit for evidence. Gradually it concedes small increments on evidence strength and allowed amount as the provider’s firm stance and the underlying clinical prior become clear. The provider, following a linear concession strategy, waits until a package appears that clears its reserved value without requiring escalation.

On step ten the provider accepts: 52% of billed, a 4% prompt-pay discount, moderate evidence credit, and no escalation. Estimated recovery is about $2,396 on a $4,800 bill. The case closes inside the system. No external review is triggered. Both agents have moved according to their designed rewards; neither has stepped outside the policy envelope encoded in the mechanism.

This is sequential decision-making under constraint. Each offer is an action. Each acceptance or rejection updates the state. The multi-agent loop produces a concrete settlement that balances recovery, cost control, evidence, and compliance — exactly the behavior a reinforcement-learning or policy-shielded negotiation system is intended to learn and improve upon.

In production the same structure can host LLM negotiators that speak in natural language while remaining bound by the same issues and utilities, or RL policies trained to maximize the defined rewards while the shields continue to enforce healthcare policy rules.

---

*Simulation run with NegMAS 0.16 SAOMechanism, AspirationNegotiator (linear) for the provider and TimeBasedConcedingNegotiator for the payer. Output captured October 2026.*
