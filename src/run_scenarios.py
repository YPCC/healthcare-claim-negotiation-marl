#!/usr/bin/env python3
"""
End-to-end showcase: run multiple IMR-grounded claim negotiation scenarios with NegMAS.
"""

import json
from pathlib import Path
from negmas_claim_negotiation import create_claim_session, run_and_report

def main():
    seeds_path = Path(__file__).parent.parent / "data" / "imr_example_seeds.json"
    with open(seeds_path) as f:
        seeds = json.load(f)

    print("Healthcare Claim Negotiation — NegMAS Multi-Scenario Showcase")
    print("=" * 60)

    for seed in seeds:
        # Slightly vary n_steps by scenario difficulty
        n_steps = 6 if seed["overturn_probability"] > 0.6 else 10
        session, _ = create_claim_session(n_steps=n_steps, seed_context=seed)
        run_and_report(session, seed)
        print("-" * 60)

    print("\nDone. Replace AspirationNegotiator / TimeBasedConcedingNegotiator")
    print("with negmas-llm agents or RL policies for full multi-turn linguistic")
    print("dialogues and trained sequential decision-making.")

if __name__ == "__main__":
    main()
