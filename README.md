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
│   └── imr_example_seeds.json          # Seed cases derived from real IMR Findings
├── src/
│   ├── generate_dataset.py            # Generate multi-turn dialogues from seeds
│   ├── negmas_claim_negotiation.py    # Core NegMAS SAO scenario
│   └── run_scenarios.py               # Run multiple negotiation scenarios end-to-end
└── examples/
    └── sample_dialogues.json            # Example generated multi-turn transcripts
```

## Quick Start

```bash
pip install -r requirements.txt

# 1. Generate synthetic multi-turn dialogues
python src/generate_dataset.py --n 20 --out data/synthetic_negotiations.jsonl

# 2. Run NegMAS end-to-end scenarios
python src/run_scenarios.py
```

## Key Components

### Dataset Generation (`src/generate_dataset.py`)
- Loads IMR-style seeds (diagnosis, Findings summary, determination prior).
- Produces multi-turn Provider Billing Specialist ↔ Insurance Adjuster dialogues.
- Annotates actions, offers, compliance flags, and outcomes.
- Covers renegotiation loops, prompt-pay settlements, and escalation.

### NegMAS Environment (`src/negmas_claim_negotiation.py`)
- Issues: `allowed_pct`, `prompt_pay_discount`, `evidence_strength`, `escalate_to_imr`.
- Opposing LinearAdditiveUtilityFunctions for Provider and Payer.
- SAOMechanism with configurable `n_steps` (appeal loops).
- Ready to swap in LLM negotiators (`negmas-llm`) or RL wrappers (`negmas-rl-tutorial`).

### Policy Shields (conceptual, enforced in environment or agent)
- ERISA / prompt-pay response deadlines
- Reference-based pricing floors
- Medical necessity / experimental criteria
- No premature escalation
- Balance-billing constraints

## Scenarios Demonstrated

| Scenario | Description | Typical Outcome Pattern |
|----------|-------------|-------------------------|
| Medical Necessity (GHD / Omnitrope style) | Strong clinical evidence | Settlement or Overturned |
| Acute Rehab | Weak evidence of acute need | Upheld denial or low offer |
| Biologic continuation (Taltz style) | Documented failure of priors | Higher recovery |
| Prompt-pay settlement | Immediate payment incentive | Faster, lower turns |
| Escalation to IMR | Internal negotiation fails | External review |

## Relation to Research

- Aligns with MA-POMDP / multi-agent sequential decision-making.
- Compatible with frameworks such as Dialogue Diplomats (arXiv:2511.17654) hierarchical consensus + progressive negotiation.
- Uses public IMR data the same way projects like Fight Health Insurance generate synthetic appeals.

## License & Disclaimer

Educational / research use only. Synthetic data. Not real patient information. Not medical, legal, or claims advice. Always verify against actual policy and regulations.

## Next Steps

- Replace classic negotiators with `negmas-llm` agents and inject full Findings text.
- Wrap with `negmas-rl-tutorial` for MARL training and retraining under policy changes.
- Scale seed extraction from the full DMHC IMR CSV.
- Add reward shaping and hard policy shields.
