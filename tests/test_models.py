import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import numpy as np
from creep_models import norton_rate, larson_miller_parameter
from stress_relaxation import simulate_fixed_strain_relaxation

def test_norton_rate_positive():
    r = norton_rate(np.array([100, 200]), A=1e-18, n=5, temperature_c=550)
    assert np.all(r > 0)
    assert r[1] > r[0]

def test_larson_miller():
    lmp = larson_miller_parameter(550, 1000)
    assert lmp > 0

def test_relaxation_decreases_stress():
    t = np.array([0, 1, 10])
    s = simulate_fixed_strain_relaxation(t, 360, params={'A':1e-16,'n':4}, temperature_c=550)
    assert s[-1] <= s[0]
