"""Constitutive creep laws for high-temperature 316H stainless steel modelling."""
from __future__ import annotations
import numpy as np
R_GAS = 8.314462618  # J/mol/K

def norton_rate(stress_mpa, A, n, Q_j_mol=0.0, temperature_c=550.0):
    """Norton creep strain rate: eps_dot = A sigma^n exp(-Q/RT)."""
    stress = np.asarray(stress_mpa, dtype=float)
    T = np.asarray(temperature_c, dtype=float) + 273.15
    return A * np.maximum(stress, 1e-12) ** n * np.exp(-Q_j_mol / (R_GAS * T))

def norton_bailey_strain(time_h, stress_mpa, A, n, m, Q_j_mol=0.0, temperature_c=550.0):
    """Norton-Bailey time hardening: eps_c = A sigma^n t^m exp(-Q/RT)."""
    t = np.asarray(time_h, dtype=float)
    stress = np.asarray(stress_mpa, dtype=float)
    T = np.asarray(temperature_c, dtype=float) + 273.15
    return A * np.maximum(stress, 1e-12) ** n * np.maximum(t, 1e-12) ** m * np.exp(-Q_j_mol / (R_GAS * T))

def garofalo_rate(stress_mpa, A, alpha, n, Q_j_mol=0.0, temperature_c=550.0):
    """Garofalo hyperbolic-sine law: eps_dot = A sinh(alpha sigma)^n exp(-Q/RT)."""
    stress = np.asarray(stress_mpa, dtype=float)
    T = np.asarray(temperature_c, dtype=float) + 273.15
    return A * np.sinh(alpha * np.maximum(stress, 0.0)) ** n * np.exp(-Q_j_mol / (R_GAS * T))

def larson_miller_parameter(temperature_c, rupture_time_h, C=20.0):
    """Larson-Miller parameter: LMP = T_K * (C + log10(t_r))."""
    T = np.asarray(temperature_c, dtype=float) + 273.15
    t = np.asarray(rupture_time_h, dtype=float)
    return T * (C + np.log10(np.maximum(t, 1e-12)))
