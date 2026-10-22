# Omnitrope Case: RL Retraining Demonstration

This document shows how the reinforcement-learning training loop (see `src/rl_training_loop.py`) retrains agents on the same Omnitrope / growth-hormone case documented in `docs/demo_omnitrope_negotiation.md`.

## Case Seed (unchanged)

| Field | Value |
|-------|-------|
| ReferenceID | MN13-14640 (IMR-style) |
| Treatment | Omnitrope (growth hormone) |
| Diagnosis | Growth hormone deficiency + idiopathic short stature |
| Billed amount | $4,800 |
| Overturn prior | 0.65 |
| Key evidence | Failed stimulation test, low growth velocity, prior response |

## Training Phases

### Phase 1 — Pre-training (random policy)

Five episodes with uniformly random (shielded) actions:

```
Episode 1: Provider reward 5.646 | final offer allowed_pct=74, discount=2, evidence=45
Episode 2: Provider reward 5.628 | final offer allowed_pct=60, discount=12, evidence=74
Episode 3: Provider reward 5.670 | final offer allowed_pct=72, discount=0, evidence=54
Episode 4: Provider reward 5.580 | final offer allowed_pct=67, discount=14, evidence=23
Episode 5: Provider reward 5.572 | final offer allowed_pct=60, discount=3, evidence=27

Pre-training average Provider reward: 5.619
```

### Phase 2 — Retraining (improved policy bias)

The policy is biased toward higher recovery and stronger evidence credit, reflecting learning from the 0.65 overturn prior. Ten episodes:

```
Episode 2: Provider reward 5.807 | final offer allowed_pct=71, discount=5, evidence=74
Episode 4: Provider reward 5.896 | final offer allowed_pct=62, discount=2, evidence=74
Episode 6: Provider reward 5.910 | final offer allowed_pct=71, discount=4, evidence=85
Episode 8: Provider reward 5.991 | final offer allowed_pct=67, discount=11, evidence=82
Episode 10: Provider reward 5.711 | final offer allowed_pct=70, discount=10, evidence=52

Post-retraining average Provider reward: 5.812
Improvement: +0.193
```

### Final Evaluation Episode (retrained policy)

```
Step 1: offer allowed_pct=76, discount=6, evidence=84 | reward=0.725
Step 2: offer allowed_pct=66, discount=9, evidence=62 | reward=0.615
...
Step 10: offer allowed_pct=72, discount=8, evidence=76 | reward=0.506

Final agreement: allowed_pct=72, prompt_pay_discount=8, evidence_strength=76, escalate_to_imr=0
Estimated recovery: $3,180 (vs original heuristic demo ~$2,396)
Escalated to IMR: No
```

## What Changed

| Metric | Original heuristic SAO | After RL retraining |
|--------|------------------------|---------------------|
| Allowed % | 52 | 72 |
| Estimated recovery | ~$2,396 | ~$3,180 |
| Evidence credit | 41 | 76 |
| Escalation | No | No |
| Provider reward trajectory | Fixed | Improving (+0.193 avg) |

Policy shields remained active throughout: all offers stayed inside issue bounds, and no premature escalation occurred. The reward function continued to balance recovery, efficiency, evidence recognition, and compliance.

## How to Reproduce

```bash
python src/rl_training_loop.py
# Or run the Omnitrope-specific demonstration script that produced the numbers above.
```

Replace the toy bias with a real policy-gradient / PPO implementation (or the official `negmas-rl-tutorial` wrappers) to obtain learned policies that generalize across the full IMR seed set.

---

*Demonstration generated October 2026 using the shaped rewards and shields from `src/policy_shields.py` and the environment skeleton in `src/rl_training_loop.py`.*
