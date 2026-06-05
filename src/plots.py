from pathlib import Path
import matplotlib.pyplot as plt

def plot_relaxation(time_h, observed, predicted, out='figures/relaxation_fit.png'):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.plot(time_h, observed, marker='o', label='observed/fixture')
    plt.plot(time_h, predicted, marker='s', label='model')
    plt.xlabel('Time [h]')
    plt.ylabel('Stress [MPa]')
    plt.title('316H stress relaxation: constitutive model fit')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=200)
    plt.close()
