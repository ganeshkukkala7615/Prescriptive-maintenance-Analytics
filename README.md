<<<<<<< HEAD
\# Prescriptive Maintenance Analytics Engine



End-to-end analytics system combining SQL-based root-cause analysis, Weibull survival modeling, cost-optimization, and Random Forest validation to recommend data-driven maintenance schedules.



\## Pipeline

1\. Synthetic data generation (Weibull-distributed failure times, 15 machines, 3 types)

2\. SQLite schema + ETL (`sql/schema.sql`, `scripts/load\_to\_db.py`)

3\. SQL root-cause analysis using window functions/CTEs (`scripts/root\_cause\_query.py`)

4\. Weibull survival analysis (`scripts/survival\_model.py`) — shape=2.26, scale=297

5\. Cost optimization via renewal-reward theorem (`scripts/cost\_optimization.py`) — optimal interval: 80 days vs 30-day baseline, ₹3.77L projected annual fleet savings

6\. Random Forest cross-validation (`scripts/threshold\_validation.py`) — F1=0.59 on 30-day failure window, recall=0.77



\## Key Findings

\- Vibration is the dominant near-term (15-day) failure signal; temperature dominates at 30-day horizon

\- SQL-identified pre-failure vibration was \~50% above fleet baseline

\- Cost-optimal inspection interval (80 days) is significantly longer than assumed baseline (30 days), driven by low early-life failure risk



\## Tech Stack

Python, SQLite, SQL (window functions, CTEs), lifelines (survival analysis), scikit-learn (Random Forest), pandas, matplotlib

=======
# Prescriptive-maintainance-Analytics
>>>>>>> 5ed625894849869981e351e14dd1f91fe37133a6
