"""Fit simple stress-relaxation laws to the real Bristol 316H summary data.

The purpose is not to claim a final constitutive law, but to demonstrate how real
high-temperature stress-relaxation measurements can be converted into a compact
calibration/validation workflow.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def exponential_relaxation(t_h: np.ndarray, sigma_inf: float, sigma0: float, tau_h: float) -> np.ndarray:
    return sigma_inf + (sigma0 - sigma_inf) * np.exp(-t_h / tau_h)


def main() -> None:
    processed = Path("data/processed")
    figures = Path("figures")
    results = Path("results")
    figures.mkdir(exist_ok=True)
    results.mkdir(exist_ok=True)
    df = pd.read_csv(processed / "bristol_316h_relaxation_summary.csv").sort_values("time_h")

    # Fit the FEA mean relaxation curve because it is smoother than the sparse ND means.
    t = df["time_h"].to_numpy(dtype=float)
    y = df["mean_fea_sVM_MPa"].to_numpy(dtype=float)
    popt, pcov = curve_fit(
        exponential_relaxation,
        t,
        y,
        p0=[float(y[-1]), float(y[0]), 500.0],
        bounds=([0.0, 0.0, 1.0], [500.0, 500.0, 1e5]),
        maxfev=20000,
    )
    yhat = exponential_relaxation(t, *popt)
    metrics = {
        "fitted_model": "sigma(t) = sigma_inf + (sigma0 - sigma_inf) exp(-t/tau)",
        "fit_target": "mean interpolated FEA von Mises stress at neutron measurement locations",
        "sigma_inf_MPa": float(popt[0]),
        "sigma0_MPa": float(popt[1]),
        "tau_h": float(popt[2]),
        "mae_MPa": float(mean_absolute_error(y, yhat)),
        "rmse_MPa": float(np.sqrt(mean_squared_error(y, yhat))),
        "r2": float(r2_score(y, yhat)),
    }
    (results / "bristol_316h_relaxation_law_fit.json").write_text(json.dumps(metrics, indent=2))

    tt = np.linspace(0, 800, 300)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(t, y, label="FEA mean at ND locations")
    ax.plot(tt, exponential_relaxation(tt, *popt), label="Fitted relaxation law")
    ax.set_xlabel("Creep exposure time at 550 °C [h]")
    ax.set_ylabel("Mean von Mises stress [MPa]")
    ax.set_title("Simple stress-relaxation law calibrated on real 316H data")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures / "bristol_316h_fitted_relaxation_law.png", dpi=200)
    plt.close(fig)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
