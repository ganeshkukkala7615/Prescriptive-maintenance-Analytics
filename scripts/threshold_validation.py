import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

conn = sqlite3.connect('outputs/maintenance.db')

query = """
SELECT s.machine_id, s.reading_time, s.vibration, s.temperature, s.rpm,
       f.failure_time, f.censored
FROM SensorReadings s
JOIN FailureEvents f ON s.machine_id = f.machine_id
"""
df = pd.read_sql(query, conn, parse_dates=['reading_time', 'failure_time'])

df['days_to_failure'] = (df['failure_time'] - df['reading_time']).dt.days
df['will_fail_soon'] = ((df['days_to_failure'] <= 30) & (df['days_to_failure'] >= 0) & (df['censored'] == 0)).astype(int)
X = df[['vibration', 'temperature', 'rpm']]
y = df['will_fail_soon']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature importance:")
print(importances)