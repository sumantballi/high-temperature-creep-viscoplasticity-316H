"""Ingest the Bristol 316H neutron-diffraction / FEA MATLAB files.

This parser converts the compact open dataset files into tidy CSV tables that can
be used for calibration, validation, and plotting. The row order follows the
Bristol readme: 800 h, 200 h, 50 h, 10 h, 1 h, 0 h, with 12 measurement locations
per condition.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io as sio

TIMES_H = [800, 200, 50, 10, 1, 0]
VOIGT = ["xx", "yy", "zz", "xy", "yz", "xz"]


def _loadmat(path: Path) -> dict:
    return sio.loadmat(path, simplify_cells=True)


def build_neutron_dataframe(raw_dir: Path) -> pd.DataFrame:
    data = _loadmat(raw_dir / "Neutron diffraction data.mat")
    locs = np.asarray(data["measurementLocs"])
    rows = []
    for block_idx, time_h in enumerate(TIMES_H):
        for loc_idx in range(locs.shape[0]):
            row_idx = block_idx * locs.shape[0] + loc_idx
            row = {
                "source": "neutron_diffraction",
                "material": "Type 316H stainless steel",
                "temperature_C": 550.0,
                "time_h": float(time_h),
                "location_id": int(loc_idx + 1),
                "x_sample": float(locs[loc_idx, 0]),
                "y_sample": float(locs[loc_idx, 1]),
                "z_sample": float(locs[loc_idx, 2]),
                "sVM_MPa": float(data["sVM"][row_idx]) / 1e6,
            }
            for i, c in enumerate(VOIGT):
                row[f"stress_{c}_MPa"] = float(data["s"][row_idx, i]) / 1e6
                row[f"stress_{c}_unc_MPa"] = float(data["us"][row_idx, i]) / 1e6
                row[f"strain_{c}"] = float(data["e"][row_idx, i])
                row[f"strain_{c}_unc"] = float(data["ue"][row_idx, i])
            rows.append(row)
    return pd.DataFrame(rows)


def build_fea_dataframe(raw_dir: Path) -> pd.DataFrame:
    data = _loadmat(raw_dir / "FEA results at measurement locations ALL (same specimen order as ND).mat")
    nd = _loadmat(raw_dir / "Neutron diffraction data.mat")
    locs = np.asarray(nd["measurementLocs"])
    rows = []
    for block_idx, time_h in enumerate(TIMES_H):
        for loc_idx in range(locs.shape[0]):
            row_idx = block_idx * locs.shape[0] + loc_idx
            row = {
                "source": "finite_element_interpolated",
                "material": "Type 316H stainless steel",
                "temperature_C": 550.0,
                "time_h": float(time_h),
                "location_id": int(loc_idx + 1),
                "x_sample": float(locs[loc_idx, 0]),
                "y_sample": float(locs[loc_idx, 1]),
                "z_sample": float(locs[loc_idx, 2]),
                "sVMFEA_MPa": float(data["sVMFEA"][row_idx]),
                "sHydFEA_MPa": float(data["sHydFEA"][row_idx]),
            }
            for i, c in enumerate(VOIGT):
                row[f"stress_fea_{c}_MPa"] = float(data["ssFEA"][row_idx, i])
                row[f"strain_fea_{c}"] = float(data["eeFEA"][row_idx, i])
            rows.append(row)
    return pd.DataFrame(rows)


def build_joined_dataframe(nd: pd.DataFrame, fea: pd.DataFrame) -> pd.DataFrame:
    keys = ["material", "temperature_C", "time_h", "location_id", "x_sample", "y_sample", "z_sample"]
    joined = nd.merge(fea.drop(columns=["source"]), on=keys, how="inner")
    joined["delta_sVM_MPa"] = joined["sVM_MPa"] - joined["sVMFEA_MPa"]
    joined["abs_delta_sVM_MPa"] = joined["delta_sVM_MPa"].abs()
    for c in ["xx", "yy", "zz"]:
        joined[f"delta_stress_{c}_MPa"] = joined[f"stress_{c}_MPa"] - joined[f"stress_fea_{c}_MPa"]
    return joined


def build_relaxation_summary(joined: pd.DataFrame) -> pd.DataFrame:
    g = joined.groupby("time_h", as_index=False).agg(
        mean_nd_sVM_MPa=("sVM_MPa", "mean"),
        std_nd_sVM_MPa=("sVM_MPa", "std"),
        mean_fea_sVM_MPa=("sVMFEA_MPa", "mean"),
        std_fea_sVM_MPa=("sVMFEA_MPa", "std"),
        mean_abs_error_sVM_MPa=("abs_delta_sVM_MPa", "mean"),
        max_abs_error_sVM_MPa=("abs_delta_sVM_MPa", "max"),
        n_locations=("location_id", "count"),
    ).sort_values("time_h")
    # A normalized relaxation ratio relative to the 0 h condition.
    s0_nd = float(g.loc[g["time_h"] == 0, "mean_nd_sVM_MPa"].iloc[0])
    s0_fea = float(g.loc[g["time_h"] == 0, "mean_fea_sVM_MPa"].iloc[0])
    g["nd_relaxation_ratio"] = g["mean_nd_sVM_MPa"] / s0_nd
    g["fea_relaxation_ratio"] = g["mean_fea_sVM_MPa"] / s0_fea
    return g


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("data/raw_external/bristol_316h_subset"))
    parser.add_argument("--out", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    nd = build_neutron_dataframe(args.raw)
    fea = build_fea_dataframe(args.raw)
    joined = build_joined_dataframe(nd, fea)
    summary = build_relaxation_summary(joined)

    nd.to_csv(args.out / "bristol_316h_neutron_stress_tensor.csv", index=False)
    fea.to_csv(args.out / "bristol_316h_fea_interpolated_stress_tensor.csv", index=False)
    joined.to_csv(args.out / "bristol_316h_joined_nd_fea.csv", index=False)
    summary.to_csv(args.out / "bristol_316h_relaxation_summary.csv", index=False)
    print(f"Wrote processed data to {args.out}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
