import sqlite3
import pandas as pd

conn = sqlite3.connect('outputs/maintenance.db')

query = """
SELECT machine_id, AVG(lifetime_days) as avg_lifetime, censored
FROM FailureEvents
GROUP BY machine_id
ORDER BY avg_lifetime ASC;
"""

df = pd.read_sql(query, conn)
print(df)

conn.close()