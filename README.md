# Healthcare Claim Negotiation Dataset & NegMAS MARL Showcase

Synthetic multi-turn **provider ↔ payer** claim negotiation dialogues and a NegMAS-based multi-agent environment for sequential decision-making / MARL under healthcare policy constraints.

Grounded in public California DMHC Independent Medical Review (IMR) data (Findings + determinations).

## Why This Exists

Real verbatim claim negotiation transcripts are proprietary and contain PHI. This repository provides:

1. A systematic way to generate realistic multi-turn negotiation / renegotiation dialogues from public IMR Findings.
2. An end-to-end NegMAS (Stacked Alternating Offers) simulation that models the process as a MA-POMDP.
3. Multiple scenarios (medical necessity, experimental, balance-bill, prompt-pay, escalation to IMR).
4. Hooks for RL / MARL training, policy shields, and retraining.
5. **Full-scale scaffolding** for the complete DMHC CSV, LLM negotiators (`negmas-llm`), and RL training loops.

## Project Structure

```
├── README.md
├── requirements.txt
├── data/
│   ├── imr_example_seeds.json
│   └── simulation_results_50.json
├── docs/
│   ├── demo_omnitrope_negotiation.md
│   └── imr_48_simulation_results.md
├── src/
│   ├── generate_dataset.py
│   ├── negmas_claim_negotiation.py
│   ├── run_scenarios.py
│   ├── load_full_imr.py          # Full DMHC CSV → seeds
│   ├── llm_negotiators.py       # negmas-llm wrappers + Findings injection
│   ├── policy_shields.py        # Hard shields + shaped rewards
│   └── rl_training_loop.py      # RL/MARL training skeleton
└── examples/
    └── sample_dialogues.json
```

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_dataset.py --n 20 --out data/synthetic_negotiations.jsonl
python src/run_scenarios.py
```

## Full-Scale Extensions

### 1. Full DMHC CSV
```bash
# Download CSV from data.chhs.ca.gov then:
python src/load_full_imr.py --csv path/to/imr.csv --max 1000 --out data/imr_full_seeds.json
```
Produces ReferenceID-linked seeds ready for NegMAS, LLM, or RL runs.

### 2. LLM Negotiators (`negmas-llm`)
```bash
pip install negmas-llm
export OPENAI_API_KEY=...
python -c "from src.llm_negotiators import run_llm_session; ..."
```
Injects real Findings into the system prompt. Supports OpenAI, Ollama, etc.

### 3. RL Training Loop
```bash
python src/rl_training_loop.py
# Or install the official tutorial package:
# pip install git+https://github.com/yasserfarouk/negmas-rl-tutorial.git
```
Minimal multi-agent environment + shaped rewards. Swap in PPO or the official NegMAS-RL wrappers.

### 4. Hardened Policy Shields & Reward Shaping
See `src/policy_shields.py`:
- Hard projection of offers into legal issue bounds
- Premature-escalation penalty
- Process rewards (efficiency, compliance) + outcome rewards (recovery / cost control)
- Reserved-value and overturn-prior modulation

## Demo & Results

- Single-case narrative: [docs/demo_omnitrope_negotiation.md](docs/demo_omnitrope_negotiation.md)
- 48 ReferenceID-linked runs: [docs/imr_48_simulation_results.md](docs/imr_48_simulation_results.md)

## Citation

```bibtex
@misc{parte2026healthcareclaimnegotiation,
  author       = {Yogesh Parte},
  title        = {Healthcare Claim Negotiation Dataset \& NegMAS MARL Showcase},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/YPCC/healthcare-claim-negotiation-marl}},
  note         = {Full DMHC IMR scaling, negmas-llm negotiators, RL training skeleton, and hardened policy shields}
}
```

## License & Disclaimer

Educational / research use only. Synthetic negotiation traces. Original IMR ReferenceIDs are public. Not medical, legal, or claims advice.
