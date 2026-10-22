#!/usr/bin/env python3
"""
Generate synthetic multi-turn healthcare claim negotiation dialogues
grounded in IMR-style Findings seeds.

Produces JSONL episodes with annotated turns, offers, actions, and outcomes.
"""

import json
import random
import argparse
from pathlib import Path
from datetime import datetime

def load_seeds(path="data/imr_example_seeds.json"):
    with open(path) as f:
        return json.load(f)

def generate_dialogue(seed, max_turns=8):
    """Simple template-based multi-turn generator (replace with LLM for higher fidelity)."""
    billed = seed["billed_amount"]
    prior = seed["overturn_probability"]
    evidence = seed["findings_summary"]

    # Provider opening
    turns = []
    turns.append({
        "turn": 1,
        "speaker": "Provider_Billing_Specialist",
        "action": "initial_appeal",
        "message": (
            f"Appealing denial of {seed['treatment']}. "
            f"{evidence} Requesting authorization at contracted or reference-based rate. "
            f"Billed amount ${billed:,}. Clinical records attached."
        ),
        "offer_pct": None,
        "compliance_ok": True
    })

    # Payer response
    initial_offer = int(55 + random.random() * 15)  # 55-70%
    turns.append({
        "turn": 2,
        "speaker": "Payer_Adjuster",
        "action": "counter_offer",
        "message": (
            f"Denial maintained under medical necessity criteria. "
            f"We can offer {initial_offer}% of billed as prompt-pay settlement "
            f"if accepted within 10 business days and further appeal is waived."
        ),
        "offer_pct": initial_offer,
        "compliance_ok": True
    })

    current_offer = initial_offer
    for t in range(3, max_turns + 1):
        if random.random() < 0.35 and current_offer >= 70:
            # Accept
            turns.append({
                "turn": t,
                "speaker": "Provider_Billing_Specialist",
                "action": "accept",
                "message": f"Accepting {current_offer}% contingent on written confirmation and no balance bill.",
                "offer_pct": current_offer,
                "compliance_ok": True
            })
            outcome = "settled"
            break
        elif random.random() < prior * 0.4 and t > 4:
            # Escalate
            turns.append({
                "turn": t,
                "speaker": "Provider_Billing_Specialist",
                "action": "escalate_to_imr",
                "message": "Internal negotiation unsuccessful. Filing for Independent Medical Review citing the clinical evidence.",
                "offer_pct": None,
                "compliance_ok": True
            })
            outcome = "escalated_to_imr"
            break
        else:
            # Counter
            if t % 2 == 1:  # Provider turn
                counter = min(95, current_offer + random.randint(5, 12))
                turns.append({
                    "turn": t,
                    "speaker": "Provider_Billing_Specialist",
                    "action": "counter_offer",
                    "message": (
                        f"Counter at {counter}% of billed. Evidence supports medical necessity. "
                        f"Alternatively we escalate."
                    ),
                    "offer_pct": counter,
                    "compliance_ok": True
                })
                current_offer = counter
            else:  # Payer turn
                counter = max(50, current_offer - random.randint(2, 8))
                turns.append({
                    "turn": t,
                    "speaker": "Payer_Adjuster",
                    "action": "counter_offer",
                    "message": f"Improved offer: {counter}% of billed as final settlement, or maintain denial.",
                    "offer_pct": counter,
                    "compliance_ok": True
                })
                current_offer = counter
    else:
        outcome = "no_agreement"

    episode = {
        "seed_id": seed["id"],
        "diagnosis": seed["diagnosis_category"],
        "treatment": seed["treatment"],
        "billed_amount": billed,
        "determination_prior": seed["determination_prior"],
        "overturn_probability": prior,
        "turns": turns,
        "final_outcome": outcome,
        "final_offer_pct": current_offer if outcome == "settled" else None,
        "n_turns": len(turns),
        "generated_at": datetime.utcnow().isoformat()
    }
    return episode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10, help="Number of episodes to generate")
    parser.add_argument("--out", type=str, default="data/synthetic_negotiations.jsonl")
    parser.add_argument("--seeds", type=str, default="data/imr_example_seeds.json")
    args = parser.parse_args()

    seeds = load_seeds(args.seeds)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    with open(args.out, "w") as f:
        for i in range(args.n):
            seed = random.choice(seeds)
            episode = generate_dialogue(seed)
            f.write(json.dumps(episode) + "\n")

    print(f"Generated {args.n} episodes → {args.out}")

if __name__ == "__main__":
    main()
