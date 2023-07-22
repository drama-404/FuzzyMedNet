# Improving Explanation of Deep Learning Models for Medical Diagnoses through Fuzzy  Logic Interpretations

├── [**data/**](./data) (CSV Files of raw and processed data) <br>
│   ├── [**processed/**](./data/processed) (contains all cleaned and preprocessed data)<br>
│   └── [**raw/**](./data/raw) (contains all raw data files)<br>

├── [**notebooks/**](./notebooks) (Jupyter notebooks for analysis, processing, training, and validation)<br>
│   ├── [**patient_stay/**](./notebooks/patient_stay) (Notebooks for Patient Stay related data - `ADMISSIONS`, `PATIENTS`, `DIAGNOSES`, etc.)<br>
│   ├── [**vital_signs/**](./notebooks/vital_signs) (Notebooks for Vital Signs related data - `CHARTEVENTS`)<br>
│   ├── [**lab_results/**](./notebooks/lab_results) (Notebooks for Lab Results related data - `LABEVENTS`)<br>
│   └── [**features/**](./notebooks/features) (Notebooks for applying Feature Importance to processed data)<br>

├── [**reports/**](./reports) (Data Visualization Graphics and Report Documents)<br>
│   └── [**figures/**](./reports/figures) (graphics from data visualization)<br>

├── [**src/**](./src) (Python scripts)<br>
│   ├── [**data/**](./src/data) (scripts to process data)<br>
│   ├── [**features/**](./src/features) (scripts to apply feature engineering)<br>
│   └── [**models/**](./src/models) (scripts to train models and then use trained models to make predictions)<br>

├── [**utils/**](./utils/) (utility scripts used across the project)<br>
│   ├── [**sql_queries/**](./utils/sql_queries) (SQL Queries executed across notebooks)<br>
│   └── [**db_connection.py**](./utils/db_connection.py) (Connect to PostGreSQL database instance for MIMIC-III dataset)<br>

├── [**config.py**](./config.py) (Constants used across the project)<br>
└── [**requirements.txt**](./requirements.txt) (Instructions to replicate Python environment)<br>
