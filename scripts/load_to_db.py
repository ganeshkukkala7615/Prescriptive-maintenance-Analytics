import sqlite3
import pandas as pd

conn = sqlite3.connect('outputs/maintenance.db')

with open('sql/schema.sql') as f:
    conn.executescript(f.read())

pd.read_csv('data/machines.csv').to_sql('Machines', conn, if_exists='append', index=False)
pd.read_csv('data/failure_events.csv').to_sql('FailureEvents', conn, if_exists='append', index=False)
pd.read_csv('data/sensor_readings.csv').to_sql('SensorReadings', conn, if_exists='append', index=False)
pd.read_csv('data/defects.csv').to_sql('Defects', conn, if_exists='append', index=False)

conn.close()
print("Database built at outputs/maintenance.db")