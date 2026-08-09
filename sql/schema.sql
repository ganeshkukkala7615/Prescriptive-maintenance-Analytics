CREATE TABLE Machines (
    machine_id INTEGER PRIMARY KEY,
    machine_type TEXT,
    line_id INTEGER,
    install_date TEXT
);

CREATE TABLE FailureEvents (
    machine_id INTEGER,
    install_time TEXT,
    failure_time TEXT,
    censored INTEGER,
    lifetime_days REAL
);

CREATE TABLE SensorReadings (
    machine_id INTEGER,
    reading_time TEXT,
    vibration REAL,
    temperature REAL,
    rpm REAL
);

CREATE TABLE Defects (
    machine_id INTEGER,
    defect_time TEXT,
    defect_type TEXT,
    severity TEXT
);