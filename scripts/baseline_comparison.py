import sqlite3
import pandas as pd

conn = sqlite3.connect('outputs/maintenance.db')

query = """
SELECT AVG(vibration) AS fleet_avg_vibration,
       AVG(temperature) AS fleet_avg_temperature
FROM SensorReadings;
"""

df = pd.read_sql(query, conn)
print("Fleet-wide average (all readings, all machines):")
print(df)
conn.close()