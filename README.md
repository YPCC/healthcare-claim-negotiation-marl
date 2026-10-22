# Healthcare Claim Negotiation Dataset & NegMAS MARL Showcase

Synthetic multi-turn **provider ↔ payer** claim negotiation dialogues and a NegMAS-based multi-agent environment for sequential decision-making / MARL under healthcare policy constraints.

Grounded in public California DMHC Independent Medical Review (IMR) data (Findings + determinations).

## Why This Exists

Real verbatim claim negotiation transcripts are proprietary and contain PHI. This repository provides:

1. A systematic way to generate realistic multi-turn negotiation / renegotiation dialogues from public IMR Findings.
2. An end-to-end NegMAS (Stacked Alternating Offers) simulation that models the process as a MA-POMDP.
3. Multiple scenarios (medical necessity, experimental, balance-bill, prompt-pay, escalation to IMR).
4. Hooks for RL / MARL training, policy shields, and retraining.

## Project Structure

```
├── README.md
├── requirements.txt
├── data/
│   ├── imr_example_seeds.json          # Seed cases derived from real IMR Findings
│   └── simulation_results_50.json       # Machine-readable results (sample + linkage)
├── docs/
│   ├── demo_omnitrope_negotiation.md   # Captured single-case simulation + narrative
│   └── imr_48_simulation_results.md    # 48 real IMR ReferenceID cases + outcomes table
├── src/
│   ├── generate_dataset.py
│   ├── negmas_claim_negotiation.py
│   └── run_scenarios.py
└── examples/
    └── sample_dialogues.json
```

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_dataset.py --n 20 --out data/synthetic_negotiations.jsonl
python src/run_scenarios.py
```

## Demo: Live Negotiation Simulation

Single-case walkthrough (Omnitrope / GHD):

**[docs/demo_omnitrope_negotiation.md](docs/demo_omnitrope_negotiation.md)**

## 48 IMR-Grounded Simulations (with ReferenceID linkage)

**[docs/imr_48_simulation_results.md](docs/imr_48_simulation_results.md)**

- 48 real DMHC IMR cases (balanced Overturned / Upheld, Medical Necessity / Experimental).
- Every row includes the public **ReferenceID** so you can look up the original Findings at https://wpso.dmhc.ca.gov/imr/.
- NegMAS SAO runs with policy constraints (issue bounds, step limits scaled by overturn prior, reserved values).
- Summary: all 48 settled; average allowed ~73%; average recovery ~$3,965; average 7 steps.
- Full table of characteristics, constraints, and outcomes is in the document above.

## Key Components

### Dataset Generation
Loads IMR-style seeds and produces annotated multi-turn Provider ↔ Payer dialogues.

### NegMAS Environment
Issues: `allowed_pct`, `prompt_pay_discount`, `evidence_strength`, `escalate_to_imr`.  
Opposing utilities + SAOMechanism. Ready for `negmas-llm` or RL wrappers.

### Policy Shields
ERISA-style step limits, issue-range enforcement, reserved-value walk-aways, medical-necessity / experimental priors.

## Scenarios Demonstrated

| Scenario | Description | Typical Outcome Pattern |
|----------|-------------|-------------------------|
| Medical Necessity (strong evidence) | High overturn prior | Higher recovery, fewer steps |
| Medical Necessity (weak evidence) | Low overturn prior | Lower recovery or more concession |
| Experimental / Investigational | EI-type IMR cases | Mixed; constrained by policy |
| Prompt-pay settlement | Immediate payment incentive | Faster close |

## Relation to Research

Aligns with MA-POMDP sequential decision-making and frameworks such as Dialogue Diplomats (arXiv:2511.17654). Uses public IMR data analogously to synthetic appeal generation projects.

## Citation

```bibtex
@misc{parte2026healthcareclaimnegotiation,
  author       = {Yogesh Parte},
  title        = {Healthcare Claim Negotiation Dataset \& NegMAS MARL Showcase},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/YPCC/healthcare-claim-negotiation-marl}},
  note         = {Includes 48 IMR-ReferenceID-linked NegMAS negotiation simulations and Omnitrope demo}
}
```

> Yogesh Parte. (2026). Healthcare Claim Negotiation Dataset & NegMAS MARL Showcase. GitHub. https://github.com/YPCC/healthcare-claim-negotiation-marl

## License & Disclaimer

Educational / research use only. Synthetic negotiation traces. Original IMR ReferenceIDs are public. Not medical, legal, or claims advice.

## Next Steps

- Scale to full DMHC CSV with LLM negotiators (`negmas-llm`).
- Add RL training loop via `negmas-rl-tutorial`.
- Harden policy shields and reward shaping.
