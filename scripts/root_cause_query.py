import sqlite3
import pandas as pd

conn = sqlite3.connect('outputs/maintenance.db')

query = """
WITH failed_machines AS (
    SELECT machine_id, failure_time
    FROM FailureEvents
    WHERE censored = 0
),
pre_failure_sensors AS (
    SELECT f.machine_id,
           s.vibration,
           s.temperature,
           s.rpm,
           s.reading_time,
           f.failure_time,
           ROW_NUMBER() OVER (
               PARTITION BY f.machine_id
               ORDER BY s.reading_time DESC
           ) AS recency_rank
    FROM failed_machines f
    JOIN SensorReadings s
      ON s.machine_id = f.machine_id
     AND s.reading_time <= f.failure_time
)
SELECT machine_id,
       AVG(vibration) AS avg_vib_before_failure,
       AVG(temperature) AS avg_temp_before_failure
FROM pre_failure_sensors
WHERE recency_rank <= 3
GROUP BY machine_id
ORDER BY avg_vib_before_failure DESC;
"""

df = pd.read_sql(query, conn)
print(df)
conn.close()