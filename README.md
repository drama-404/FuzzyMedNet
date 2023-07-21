# Improving Explanation of Deep Learning Models for Medical Diagnoses through Fuzzy  Logic Interpretations


├── **data/** (CSV Files of raw and processed data) <br>
│   ├── **processed/** (contains all cleaned and preprocessed data)<br>
│   └── **raw/** (contains all raw data files)<br>

├── **notebooks/** (Jupyter notebooks for analysis, processing, training, and validation)<br>
│   ├── **patient_stay/** (Notebooks for Patient Stay related data - `ADMISSIONS`, `PATIENTS`, `DIAGNOSES`, etc.)<br>
│   ├── **vital_signs/** (Notebooks for Vital Signs related data - `CHARTEVENTS`)<br>
│   ├── **lab_results/** (Notebooks for Lab Results related data - `LABEVENTS`)<br>
│   └── **features/** (Notebooks for applying Feature Importance to processed data)<br>

├── **reports/** (Data Visualization Graphics and Report Documents)<br>
│   └── **figures/** (graphics from data visualization)<br>

├── **src/** (Python scripts)<br>
│   ├── **data/** (scripts to process data)<br>
│   ├── **features/** (scripts to apply feature engineering)<br>
│   └── **models/** (scripts to train models and then use trained models to make predictions)<br>

├── **utils/** (utility scripts used across the project)<br>
│   ├── **sql_queries/** (SQL Queries executed across notebooks)<br>
│   └── **db_connection.py** (Connect to PostGreSQL database instance for MIMIC-III dataset)<br>

├── **.gitignore**<br>
├── **config.py** (Constants used across the project)<br>
└── **requirements.txt** (Instructions to replicate Python environment)<br>
