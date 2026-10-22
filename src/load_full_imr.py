#!/usr/bin/env python3
"""
Scale to full DMHC Independent Medical Review (IMR) CSV.

Download the public CSV from:
https://data.chhs.ca.gov/dataset/independent-medical-review-imr-determinations-trend
(or the curated ZenML / Kaggle mirrors).

This module loads it, extracts structured seeds with ReferenceID linkage,
and prepares them for NegMAS + LLM / RL runs.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

def load_imr_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    required = ["ReferenceID", "Determination", "Type", "Findings"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")
    return df.dropna(subset=["ReferenceID", "Findings"]).copy()

def row_to_seed(row: pd.Series, billed_base: int = 5000) -> Dict[str, Any]:
    det = str(row.get("Determination", ""))
    overturn_prob = 0.65 if "Overturned" in det else 0.30
    findings = str(row.get("Findings", ""))[:800]
    return {
        "reference_id": row["ReferenceID"],
        "report_year": row.get("ReportYear"),
        "diagnosis_category": row.get("DiagnosisCategory"),
        "treatment_category": row.get("TreatmentCategory"),
        "imr_type": row.get("Type"),
        "imr_determination": det,
        "overturn_probability": overturn_prob,
        "findings_summary": findings,
        "billed_amount": billed_base,
        "imr_lookup": f"https://wpso.dmhc.ca.gov/imr/ (ReferenceID: {row['ReferenceID']})",
    }

def generate_seeds_from_csv(
    csv_path: str,
    out_path: str = "data/imr_full_seeds.json",
    max_rows: int = 500,
    stratify: bool = True,
) -> List[Dict[str, Any]]:
    df = load_imr_csv(csv_path)
    if stratify and "Determination" in df.columns and "Type" in df.columns:
        samples = []
        for det in df["Determination"].unique():
            for typ in df["Type"].unique():
                sub = df[(df["Determination"] == det) & (df["Type"] == typ)]
                n = min(max(1, max_rows // 8), len(sub))
                if n:
                    samples.append(sub.sample(n=n, random_state=42))
        df = pd.concat(samples).drop_duplicates(subset=["ReferenceID"]).head(max_rows)
    else:
        df = df.sample(n=min(max_rows, len(df)), random_state=42)

    seeds = [row_to_seed(r) for _, r in df.iterrows()]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(seeds, f, indent=2)
    print(f"Wrote {len(seeds)} IMR-linked seeds → {out_path}")
    return seeds

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, help="Path to full DMHC IMR CSV")
    p.add_argument("--out", default="data/imr_full_seeds.json")
    p.add_argument("--max", type=int, default=500)
    args = p.parse_args()
    generate_seeds_from_csv(args.csv, args.out, args.max)
