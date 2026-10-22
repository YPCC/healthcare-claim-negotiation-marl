# Omnitrope Case — Three-Minute Techno-Functional Story Script

**Narration length:** ~2 min 42 s  
**Voice:** Leo  
**Visuals:** Journey infographic → System architecture → Retraining snapshot

---

## Script

Healthcare claim negotiations have always been a human bottleneck. When a provider bills for Omnitrope growth hormone therapy for a child with documented growth hormone deficiency, the claim often lands in a denial queue. Billing specialists and payer adjusters then spend hours on phone calls and portal messages. They trade offers, cite clinical notes, and try to stay inside ERISA timelines and medical-necessity rules. Every case is different, yet the process is repetitive. Protected health information stays locked inside proprietary systems, so no one can easily learn from prior outcomes. The result is slow settlements, inconsistent recovery, and frequent escalations to independent medical review.

Now imagine two software agents taking over the structured part of that work. One represents the provider, the other the payer. They negotiate over four explicit issues: allowed percentage, prompt-pay discount, evidence strength, and whether to escalate to external review. Hard policy shields prevent them from proposing illegal values. In the original Omnitrope demonstration, these agents reached a compliant settlement of fifty-two percent allowed, roughly two thousand four hundred dollars recovered, in ten steps, with no escalation. Humans remain in the loop only for clinical judgment and final approval. The agents handle the repetitive offer loop, produce an auditable trail, and stay inside the regulatory envelope.

The final step is reinforcement learning. The same agents are placed in a multi-agent training loop. They experience many episodes of the Omnitrope case and similar IMR-grounded seeds. A shaped reward function credits higher recovery, faster closure, recognition of clinical evidence, and compliance. Policy shields continue to block illegal actions. After retraining, the provider agent learns to hold for stronger terms when the overturn prior is high. In the evaluation episode the final agreement rises to seventy-two percent allowed, estimated recovery climbs to about three thousand one hundred eighty dollars, and evidence credit improves from forty-one to seventy-six, still without escalation. Average provider reward increases by zero point one nine three.

The architecture is simple and powerful. Public IMR findings seed the cases. A negotiation environment with shields hosts the agents. An RL training loop improves their policies. Optional large-language-model negotiators can speak in natural language while remaining bound by the same issues and rewards. Humans set the policy bounds and review exceptions. The result is sequential decision-making that scales, assists the experts, and continuously improves under real healthcare constraints.

---

## Key Numbers Used

| Stage | Allowed % | Estimated Recovery | Evidence Credit | Escalation | Notes |
|-------|-----------|--------------------|-----------------|------------|-------|
| Human process | — | Inconsistent | — | Frequent | Hours of manual work |
| Agent-assisted SAO | 52 | ~$2,396 | 41 | No | 10 steps |
| After RL retraining | 72 | ~$3,180 | 76 | No | +0.193 avg reward |

## Visual Sequence

1. **0:00–0:54** — Journey infographic (Human → Agents → RL)
2. **0:54–1:48** — Solution architecture diagram
3. **1:48–2:42** — Retraining snapshot dashboard

---

*Script and video produced October 2026. Numbers grounded in the NegMAS SAO demo and the RL retraining demonstration in this repository.*
