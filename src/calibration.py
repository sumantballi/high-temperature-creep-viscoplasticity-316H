"""Parameter calibration utilities for creep/stress-relaxation data."""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares
from stress_relaxation import simulate_fixed_strain_relaxation

def fit_relaxation_norton(time_h, stress_mpa, temperature_c=550.0, E_mpa=155000.0):
    """Fit A and n for a fixed-strain Norton relaxation model."""
    time = np.asarray(time_h, dtype=float)
    stress = np.asarray(stress_mpa, dtype=float)
    sigma0 = float(stress[0])

    def residual(theta):
        logA, n = theta
        pred = simulate_fixed_strain_relaxation(time, sigma0, E_mpa=E_mpa, law='norton', params={'A': 10**logA, 'n': n}, temperature_c=temperature_c)
        return (pred - stress) / max(np.std(stress), 1.0)

    res = least_squares(residual, x0=[-16, 4.0], bounds=([-30, 1.0], [-5, 15.0]))
    return {'A': 10**res.x[0], 'n': res.x[1], 'cost': res.cost, 'success': res.success}

def regression_metrics(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    err = y_pred - y_true
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err**2)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((y_true - np.mean(y_true))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return {'mae': mae, 'rmse': rmse, 'r2': r2}
