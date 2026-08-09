import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)
N_MACHINES = 15
MACHINE_TYPES = ['Bearing', 'Gearbox', 'Motor']

machines = pd.DataFrame({
    'machine_id': range(1, N_MACHINES+1),
    'machine_type': np.random.choice(MACHINE_TYPES, N_MACHINES),
    'line_id': np.random.randint(1, 4, N_MACHINES),
    'install_date': [datetime(2024,1,1) + timedelta(days=int(x)) for x in np.random.randint(0,30,N_MACHINES)]
})

# Weibull failure times per machine type (shape > 1 = wear-out behavior)
shape_map = {'Bearing': 2.5, 'Gearbox': 1.8, 'Motor': 3.0}
scale_map = {'Bearing': 180, 'Gearbox': 250, 'Motor': 300}

failure_events = []
sensor_readings = []
defects = []

for _, m in machines.iterrows():
    shape = shape_map[m['machine_type']]
    scale = scale_map[m['machine_type']]
    lifetime = np.random.weibull(shape) * scale
    censored = lifetime > 365  # simulate 1-year observation window
    lifetime = min(lifetime, 365)
    failure_time = m['install_date'] + timedelta(days=lifetime)

    failure_events.append({
        'machine_id': m['machine_id'],
        'install_time': m['install_date'],
        'failure_time': failure_time if not censored else None,
        'censored': censored,
        'lifetime_days': lifetime
    })

    # Sensor readings ramping up as failure approaches
    for day in range(0, int(lifetime), 5):
        stress_factor = day / lifetime
        sensor_readings.append({
            'machine_id': m['machine_id'],
            'reading_time': m['install_date'] + timedelta(days=day),
            'vibration': 2 + stress_factor*5 + np.random.normal(0,0.3),
            'temperature': 40 + stress_factor*20 + np.random.normal(0,1.5),
            'rpm': 1000 + np.random.normal(0,20)
        })
        if np.random.rand() < 0.05 + stress_factor*0.15:
            defects.append({
                'machine_id': m['machine_id'],
                'defect_time': m['install_date'] + timedelta(days=day),
                'defect_type': np.random.choice(['Crack','Misalign','Overheat']),
                'severity': np.random.choice(['Low','Medium','High'])
            })

machines.to_csv('data/machines.csv', index=False)
pd.DataFrame(failure_events).to_csv('data/failure_events.csv', index=False)
pd.DataFrame(sensor_readings).to_csv('data/sensor_readings.csv', index=False)
pd.DataFrame(defects).to_csv('data/defects.csv', index=False)

print("Data generated in /data")