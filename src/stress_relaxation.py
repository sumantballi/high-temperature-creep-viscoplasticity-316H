"""Stress-relaxation model under fixed total strain."""
from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
from creep_models import norton_rate, garofalo_rate

def simulate_fixed_strain_relaxation(time_h, sigma0_mpa, E_mpa=155000.0, law='norton', params=None, temperature_c=550.0):
    """Integrate dσ/dt = -E * eps_dot_creep(σ,T) for fixed total strain.

    Time is in hours. Creep strain rate is interpreted as 1/hour for this repository.
    """
    params = params or {}
    t_eval = np.asarray(time_h, dtype=float)
    t_span = (float(np.min(t_eval)), float(np.max(t_eval)))
    if t_span[0] == t_span[1]:
        return np.full_like(t_eval, sigma0_mpa, dtype=float)

    def rhs(t, y):
        sigma = max(float(y[0]), 0.0)
        if law == 'norton':
            rate = norton_rate(sigma, params.get('A', 1e-20), params.get('n', 5.0), params.get('Q', 0.0), temperature_c)
        elif law == 'garofalo':
            rate = garofalo_rate(sigma, params.get('A', 1e-8), params.get('alpha', 0.01), params.get('n', 3.0), params.get('Q', 0.0), temperature_c)
        else:
            raise ValueError(f'Unknown law: {law}')
        return [-E_mpa * float(rate)]

    sol = solve_ivp(rhs, t_span, [sigma0_mpa], t_eval=t_eval, rtol=1e-7, atol=1e-9, method='RK45')
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0]
