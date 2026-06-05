"""Lightweight parsers for downloaded Abaqus text outputs.

Abaqus .dat files vary by export settings. This parser extracts numeric lines and creates
summary features that can be used for exploratory modelling.
"""
from __future__ import annotations
import argparse, re
from pathlib import Path
import pandas as pd
import numpy as np

FLOAT_RE = re.compile(r"[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?|[-+]?\d+(?:[Ee][-+]?\d+)")

def extract_numeric_lines(path: Path):
    rows = []
    for i, line in enumerate(path.read_text(errors='ignore').splitlines(), start=1):
        nums = [float(x) for x in FLOAT_RE.findall(line)]
        if len(nums) >= 3:
            rows.append({'file': path.name, 'line': i, 'n_values': len(nums), 'min': min(nums), 'max': max(nums), 'mean': float(np.mean(nums))})
    return rows

def parse_directory(raw: Path) -> pd.DataFrame:
    rows = []
    for p in raw.rglob('*'):
        if p.suffix.lower() in {'.dat', '.inp', '.for', '.txt'} and p.is_file():
            rows.extend(extract_numeric_lines(p))
    return pd.DataFrame(rows)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw', default='data/raw_external/bristol_316h')
    ap.add_argument('--out', default='data/processed/bristol_316h_numeric_summary.csv')
    args = ap.parse_args()
    df = parse_directory(Path(args.raw))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f'Wrote {len(df)} numeric rows to {args.out}')
