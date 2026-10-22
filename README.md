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
6. **Verbal multi-turn transcripts** generated from structured NegMAS outcomes.

## Project Structure

```
├── README.md
├── requirements.txt
├── data/
│   ├── imr_example_seeds.json
│   └── simulation_results_50.json
├── docs/
│   ├── demo_omnitrope_negotiation.md
│   ├── imr_48_simulation_results.md
│   ├── omnitrope_marl_story.mp4
│   ├── omnitrope_marl_story_narrated.mp4
│   ├── omnitrope_negotiation_dialogue_video.mp4
│   ├── omnitrope_three_min_story.mp4
│   ├── omnitrope_retraining_demo.md
│   └── omnitrope_three_min_story_script.md
├── src/
│   ├── generate_dataset.py
│   ├── negmas_claim_negotiation.py
│   ├── run_scenarios.py
│   ├── load_full_imr.py
│   ├── llm_negotiators.py
│   ├── policy_shields.py
│   ├── rl_training_loop.py
│   └── generate_verbal_transcript.py
└── examples/
    ├── sample_dialogues.json
    └── omnitrope_verbal_transcript.txt
```

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_dataset.py --n 20 --out data/synthetic_negotiations.jsonl
python src/run_scenarios.py
python src/generate_verbal_transcript.py
```

## Full-Scale Extensions

### 1. Full DMHC CSV
```bash
python src/load_full_imr.py --csv path/to/imr.csv --max 1000 --out data/imr_full_seeds.json
```

### 2. LLM Negotiators (`negmas-llm`)
```bash
pip install negmas-llm
export OPENAI_API_KEY=...
```

### 3. RL Training Loop
```bash
python src/rl_training_loop.py
```

### 4. Verbal Multi-Turn Transcripts
```bash
python src/generate_verbal_transcript.py
```
Converts structured NegMAS offer history into realistic Provider ↔ Payer natural-language dialogue grounded in the IMR Findings and the negotiated numbers.

## Demo & Results

- Single-case narrative: [docs/demo_omnitrope_negotiation.md](docs/demo_omnitrope_negotiation.md)
- Verbal transcript example: [examples/omnitrope_verbal_transcript.txt](examples/omnitrope_verbal_transcript.txt)
- **Videos**:
  - MARL story: [docs/omnitrope_marl_story.mp4](docs/omnitrope_marl_story.mp4)
  - Narrated MARL story: [docs/omnitrope_marl_story_narrated.mp4](docs/omnitrope_marl_story_narrated.mp4)
  - Multi-turn negotiation dialogue: [docs/omnitrope_negotiation_dialogue_video.mp4](docs/omnitrope_negotiation_dialogue_video.mp4)
  - 3-minute techno-functional story: [docs/omnitrope_three_min_story.mp4](docs/omnitrope_three_min_story.mp4)
- 48 ReferenceID-linked runs: [docs/imr_48_simulation_results.md](docs/imr_48_simulation_results.md)

## Citation

```bibtex
@misc{parte2026healthcareclaimnegotiation,
  author       = {Yogesh Parte},
  title        = {Healthcare Claim Negotiation Dataset \& NegMAS MARL Showcase},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/YPCC/healthcare-claim-negotiation-marl}},
  note         = {Includes verbal multi-turn transcripts, narrated videos, full DMHC IMR scaling, negmas-llm, RL training, and hardened policy shields}
}
```

## License & Disclaimer

Educational / research use only. Synthetic negotiation traces. Original IMR ReferenceIDs are public. Not medical, legal, or claims advice.
