import sqlite3
import pandas as pd
from lifelines import WeibullFitter
import matplotlib.pyplot as plt

conn = sqlite3.connect('outputs/maintenance.db')
df = pd.read_sql('SELECT * FROM FailureEvents', conn)

wf = WeibullFitter()
wf.fit(durations=df['lifetime_days'], event_observed=~df['censored'].astype(bool))

print(f"Shape (rho): {wf.rho_:.3f}, Scale (lambda): {wf.lambda_:.3f}")

wf.plot_survival_function()
plt.title("Machine Survival Curve")
plt.savefig('outputs/survival_curve.png')
print("Saved outputs/survival_curve.png")