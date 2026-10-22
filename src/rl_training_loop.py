#!/usr/bin/env python3
"""
RL / MARL training loop skeleton for claim negotiation.

Inspired by https://github.com/yasserfarouk/negmas-rl-tutorial
(AAMAS 2025 tutorial on Reinforcement Learning for Automated Negotiation).

This is a minimal gym-style wrapper + simple policy-gradient sketch.
Replace the policy with a proper PPO / Q-learning implementation or
the official negmas-rl-tutorial wrappers when available.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from src.policy_shields import (
    shaped_provider_reward,
    shaped_payer_reward,
    apply_shields_to_offer,
    ISSUE_BOUNDS,
)

class ClaimNegotiationEnv:
    """Minimal multi-agent environment wrapping a NegMAS-style session."""

    def __init__(self, seed: Dict[str, Any], max_steps: int = 10):
        self.seed = seed
        self.max_steps = max_steps
        self.reset()

    def reset(self):
        self.step_count = 0
        self.current_offer = {"allowed_pct": 60, "prompt_pay_discount": 10,
                              "evidence_strength": 30, "escalate_to_imr": 0}
        self.done = False
        return self._obs()

    def _obs(self) -> Dict[str, float]:
        return {
            "step_frac": self.step_count / self.max_steps,
            "allowed_pct": self.current_offer["allowed_pct"] / 120.0,
            "discount": self.current_offer["prompt_pay_discount"] / 25.0,
            "evidence": self.current_offer["evidence_strength"] / 100.0,
            "prior": self.seed.get("overturn_probability", 0.5),
        }

    def step(self, provider_action: Dict, payer_action: Dict) -> Tuple[Dict, float, float, bool]:
        # Alternate who moves; here both propose and we take a simple merge
        new_offer = apply_shields_to_offer({
            "allowed_pct": int((provider_action.get("allowed_pct", 70) + payer_action.get("allowed_pct", 60)) / 2),
            "prompt_pay_discount": int(payer_action.get("discount", 5)),
            "evidence_strength": int(provider_action.get("evidence", 40)),
            "escalate_to_imr": int(provider_action.get("escalate", 0)),
        })
        self.current_offer = new_offer
        self.step_count += 1
        self.done = self.step_count >= self.max_steps or new_offer["escalate_to_imr"] == 1

        r_prov = shaped_provider_reward(
            new_offer, self.seed.get("billed_amount", 5000),
            self.step_count, self.max_steps,
            self.seed.get("overturn_probability", 0.5),
        )
        r_pay = shaped_payer_reward(
            new_offer, self.seed.get("billed_amount", 5000),
            self.step_count, self.max_steps,
        )
        return self._obs(), r_prov, r_pay, self.done

def simple_policy_gradient_demo(seeds: List[Dict], episodes: int = 20):
    """Toy training loop that logs average reward improvement."""
    print("Running toy MARL loop (replace with real PPO / negmas-rl-tutorial)")
    history = []
    for ep in range(episodes):
        seed = seeds[ep % len(seeds)]
        env = ClaimNegotiationEnv(seed)
        obs = env.reset()
        ep_r_prov, ep_r_pay = 0.0, 0.0
        while not env.done:
            # Random shielded actions for demo
            prov_act = {"allowed_pct": np.random.randint(55, 95),
                        "evidence": np.random.randint(20, 80),
                        "escalate": 0}
            pay_act = {"allowed_pct": np.random.randint(50, 80),
                       "discount": np.random.randint(0, 15)}
            obs, rp, ry, done = env.step(prov_act, pay_act)
            ep_r_prov += rp
            ep_r_pay += ry
        history.append((ep_r_prov, ep_r_pay))
        if (ep + 1) % 5 == 0:
            avg_p = np.mean([h[0] for h in history[-5:]])
            avg_y = np.mean([h[1] for h in history[-5:]])
            print(f"Episode {ep+1}: avg Provider reward {avg_p:.3f} | Payer {avg_y:.3f}")
    return history

if __name__ == "__main__":
    demo_seeds = [{"reference_id": "DEMO", "overturn_probability": 0.6, "billed_amount": 4800}]
    simple_policy_gradient_demo(demo_seeds, episodes=10)
