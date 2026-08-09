import numpy as np
import matplotlib.pyplot as plt
from lifelines import WeibullFitter
import sqlite3
import pandas as pd

conn = sqlite3.connect('outputs/maintenance.db')
df = pd.read_sql('SELECT * FROM FailureEvents', conn)

wf = WeibullFitter()
wf.fit(durations=df['lifetime_days'], event_observed=~df['censored'].astype(bool))

cost_inspection = 5000
cost_failure = 80000

intervals = np.arange(5, 120, 5)
daily_costs = []
for t in intervals:
    p_fail = wf.cumulative_density_at_times(t).iloc[0]
    # Renewal-reward: expected cost PER DAY, not per single decision
    cost_per_day = (cost_inspection + p_fail * cost_failure) / t
    daily_costs.append(cost_per_day)

annual_costs = [c * 365 for c in daily_costs]

best_idx = np.argmin(daily_costs)
print(f"Optimal inspection interval: {intervals[best_idx]} days")
print(f"Expected cost/day at optimum: ₹{daily_costs[best_idx]:.2f}")
print(f"Projected annual cost at optimum: ₹{annual_costs[best_idx]:.0f}")

# Compare against a naive baseline (e.g., current practice = every 30 days)
baseline_t = 30
p_fail_baseline = wf.cumulative_density_at_times(baseline_t).iloc[0]
baseline_annual = ((cost_inspection + p_fail_baseline*cost_failure) / baseline_t) * 365
savings = baseline_annual - annual_costs[best_idx]
print(f"Baseline (30-day) annual cost: ₹{baseline_annual:.0f}")
print(f"Projected annual savings: ₹{savings:.0f}")

plt.plot(intervals, annual_costs)
plt.axvline(intervals[best_idx], color='red', linestyle='--', label=f'Optimal: {intervals[best_idx]} days')
plt.axvline(baseline_t, color='gray', linestyle=':', label='Baseline: 30 days')
plt.xlabel("Inspection Interval (days)")
plt.ylabel("Projected Annual Cost (₹)")
plt.title("Cost-Optimal Inspection Interval")
plt.legend()
plt.savefig('outputs/cost_curve.png')
print("Saved outputs/cost_curve.png")