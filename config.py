"""
config.py

This module stores all constants used across the project.
"""
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONNECTION_DIR = os.path.join(BASE_DIR, 'utils/')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data/processed/')
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data/all_hourly_data.h5')

FIG_DIR = os.path.join(BASE_DIR, 'reports/figures/')
FIG_PATIENT_STAY_DIR = os.path.join(FIG_DIR, 'patient_stay/')
FIG_DIAGNOSES_DIR = os.path.join(FIG_DIR, 'diagnoses/')
FIG_VITAL_SIGNS_DIR = os.path.join(FIG_DIR, 'vital_signs/')
FIG_LAB_RESULTS_DIR = os.path.join(FIG_DIR, 'lab_results/')

PROCESSING_DIR = os.path.join(BASE_DIR, 'src/data/')

SCRIPTS_DIR = os.path.join(BASE_DIR, 'SQL_Queries')
SCRIPTS_VITAL_SIGNS_DIR = os.path.join(SCRIPTS_DIR, 'vital_signs/')
SCRIPTS_LAB_RESULTS_DIR = os.path.join(SCRIPTS_DIR, 'lab_results/')


