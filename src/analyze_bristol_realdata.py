"""Generate real-data validation figures for the Bristol 316H dataset."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def main() -> None:
    processed = Path("data/processed")
    figures = Path("figures")
    results = Path("results")
    figures.mkdir(exist_ok=True)
    results.mkdir(exist_ok=True)

    joined = pd.read_csv(processed / "bristol_316h_joined_nd_fea.csv")
    summary = pd.read_csv(processed / "bristol_316h_relaxation_summary.csv")

    y = joined["sVM_MPa"].to_numpy()
    yhat = joined["sVMFEA_MPa"].to_numpy()
    metrics = {
        "dataset": "Bristol 316H neutron diffraction and interpolated FEA at 550 C",
        "n_measurements": int(len(joined)),
        "temperature_C": 550.0,
        "mae_sVM_MPa": float(mean_absolute_error(y, yhat)),
        "rmse_sVM_MPa": float(np.sqrt(mean_squared_error(y, yhat))),
        "r2_sVM": float(r2_score(y, yhat)),
    }
    (results / "bristol_316h_realdata_metrics.json").write_text(json.dumps(metrics, indent=2))

    # Relaxation evolution.
    fig, ax = plt.subplots(figsize=(7, 4.5))
    s = summary.sort_values("time_h")
    ax.errorbar(s["time_h"], s["mean_nd_sVM_MPa"], yerr=s["std_nd_sVM_MPa"], marker="o", label="Neutron diffraction")
    ax.errorbar(s["time_h"], s["mean_fea_sVM_MPa"], yerr=s["std_fea_sVM_MPa"], marker="s", label="FEA interpolated")
    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlabel("Creep exposure time at 550 °C [h]")
    ax.set_ylabel("Mean von Mises stress [MPa]")
    ax.set_title("316H stress relaxation: neutron diffraction vs FEA")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(figures / "bristol_316h_stress_relaxation_nd_vs_fea.png", dpi=200)
    plt.close(fig)

    # Predicted vs measured.
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(joined["sVM_MPa"], joined["sVMFEA_MPa"], alpha=0.75)
    lo = min(joined["sVM_MPa"].min(), joined["sVMFEA_MPa"].min())
    hi = max(joined["sVM_MPa"].max(), joined["sVMFEA_MPa"].max())
    ax.plot([lo, hi], [lo, hi], linestyle="--")
    ax.set_xlabel("Measured von Mises stress, ND [MPa]")
    ax.set_ylabel("Interpolated FEA von Mises stress [MPa]")
    ax.set_title("Model validation at neutron measurement points")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(figures / "bristol_316h_fea_vs_neutron_svm.png", dpi=200)
    plt.close(fig)

    # Location-wise residuals.
    pivot = joined.pivot_table(index="location_id", columns="time_h", values="delta_sVM_MPa", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(pivot.to_numpy(), aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([str(int(c)) for c in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([str(int(i)) for i in pivot.index])
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Measurement location")
    ax.set_title("ND - FEA von Mises stress residuals [MPa]")
    fig.colorbar(im, ax=ax, label="Residual [MPa]")
    fig.tight_layout()
    fig.savefig(figures / "bristol_316h_location_residuals_heatmap.png", dpi=200)
    plt.close(fig)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
