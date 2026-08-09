import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from lifelines import WeibullFitter

st.set_page_config(page_title="Prescriptive Maintenance Analytics", layout="wide")
st.title("🔧 Prescriptive Maintenance Analytics Dashboard")

conn = sqlite3.connect('outputs/maintenance.db')

# --- Load data ---
failures = pd.read_sql('SELECT * FROM FailureEvents', conn)

# --- Survival model ---
wf = WeibullFitter()
wf.fit(durations=failures['lifetime_days'], event_observed=~failures['censored'].astype(bool))

col1, col2, col3 = st.columns(3)
col1.metric("Weibull Shape (ρ)", f"{wf.rho_:.2f}")
col2.metric("Weibull Scale (λ)", f"{wf.lambda_:.1f} days")
col3.metric("Machines Analyzed", len(failures))

st.subheader("Survival Curve")
fig1, ax1 = plt.subplots()
wf.plot_survival_function(ax=ax1)
ax1.set_xlabel("Days")
ax1.set_ylabel("Probability of Survival")
st.pyplot(fig1)

# --- Cost optimization ---
st.subheader("Cost-Optimal Inspection Interval")
cost_inspection = st.slider("Inspection cost (₹)", 1000, 20000, 5000, step=500)
cost_failure = st.slider("Failure cost (₹)", 20000, 200000, 80000, step=5000)

intervals = np.arange(5, 120, 5)
annual_costs = []
for t in intervals:
    p_fail = wf.cumulative_density_at_times(t).iloc[0]
    cost_per_day = (cost_inspection + p_fail * cost_failure) / t
    annual_costs.append(cost_per_day * 365)

best_idx = np.argmin(annual_costs)
baseline_t = 30
p_fail_baseline = wf.cumulative_density_at_times(baseline_t).iloc[0]
baseline_annual = ((cost_inspection + p_fail_baseline*cost_failure) / baseline_t) * 365
savings = baseline_annual - annual_costs[best_idx]

colA, colB, colC = st.columns(3)
colA.metric("Optimal Interval", f"{intervals[best_idx]} days")
colB.metric("Projected Annual Cost", f"₹{annual_costs[best_idx]:,.0f}")
colC.metric("Savings vs 30-day baseline", f"₹{savings:,.0f}")

fig2, ax2 = plt.subplots()
ax2.plot(intervals, annual_costs)
ax2.axvline(intervals[best_idx], color='red', linestyle='--', label=f'Optimal: {intervals[best_idx]}d')
ax2.axvline(baseline_t, color='gray', linestyle=':', label='Baseline: 30d')
ax2.set_xlabel("Inspection Interval (days)")
ax2.set_ylabel("Projected Annual Cost (₹)")
ax2.legend()
st.pyplot(fig2)

# --- Root cause ---
st.subheader("Pre-Failure Sensor Signature (SQL Root-Cause Analysis)")
query = """
WITH failed_machines AS (
    SELECT machine_id, failure_time FROM FailureEvents WHERE censored = 0
),
pre_failure_sensors AS (
    SELECT f.machine_id, s.vibration, s.temperature,
           ROW_NUMBER() OVER (PARTITION BY f.machine_id ORDER BY s.reading_time DESC) AS recency_rank
    FROM failed_machines f
    JOIN SensorReadings s ON s.machine_id = f.machine_id AND s.reading_time <= f.failure_time
)
SELECT machine_id, AVG(vibration) AS avg_vib_before_failure, AVG(temperature) AS avg_temp_before_failure
FROM pre_failure_sensors WHERE recency_rank <= 3
GROUP BY machine_id ORDER BY avg_vib_before_failure DESC;
"""
root_cause_df = pd.read_sql(query, conn)
st.dataframe(root_cause_df, use_container_width=True)

conn.close()