from pathlib import Path
import json
import pandas as pd
from calibration import fit_relaxation_norton, regression_metrics
from stress_relaxation import simulate_fixed_strain_relaxation
from plots import plot_relaxation

fixture = Path('data/fixtures/stress_relaxation_fixture.csv')
df = pd.read_csv(fixture)
fit = fit_relaxation_norton(df.time_h, df.stress_mpa, temperature_c=550.0)
pred = simulate_fixed_strain_relaxation(df.time_h, df.stress_mpa.iloc[0], params=fit, temperature_c=550.0)
metrics = regression_metrics(df.stress_mpa, pred)
Path('results').mkdir(exist_ok=True)
Path('figures').mkdir(exist_ok=True)
plot_relaxation(df.time_h, df.stress_mpa, pred)
with open('results/demo_metrics.json','w') as f:
    json.dump({'fit': fit, 'metrics': metrics}, f, indent=2)
print({'fit': fit, 'metrics': metrics})
