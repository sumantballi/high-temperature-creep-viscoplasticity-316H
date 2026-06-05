"""Download selected real-data files from the University of Bristol 316H dataset.

The complete dataset is ~215 MB, so this script downloads a curated subset of text files.
Respect the dataset licence and cite the DOI in derived work.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import requests

BASE = "https://data.bris.ac.uk/datasets/rhg1bk2424a6262ecb9nouzp9"
FILES = [
    "Readme.txt",
    "Finite%20element%20modelling/1%20hour/316H_R66_simplified_2.for",
    "Finite%20element%20modelling/1%20hour/CreepDCB1Job1.dat",
    "Finite%20element%20modelling/1%20hour/CreepDCB1Job1.inp",
    "Finite%20element%20modelling/10%20hours/CreepDCB1Job1.dat",
    "Finite%20element%20modelling/50%20hours/CreepDCB1Job1.dat",
    "Finite%20element%20modelling/200%20hours/CreepDCB1Job1.dat",
    "Finite%20element%20modelling/800%20hours/CreepDCB1Job1.dat",
]

def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    target.write_bytes(r.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/raw_external/bristol_316h")
    args = parser.parse_args()
    out = Path(args.out)
    for rel in FILES:
        url = f"{BASE}/{rel}"
        local_name = rel.replace("%20", "_").replace("/", "__")
        print(f"Downloading {url}")
        try:
            download(url, out / local_name)
        except Exception as exc:
            print(f"WARNING: failed to download {url}: {exc}")
    print("Done. Review licence and citation requirements before publishing derived data.")
