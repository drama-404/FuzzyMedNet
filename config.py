"""
config.py

This module stores all constants used across the project.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONNECTION_DIR = os.path.join(BASE_DIR, 'utils/')
DATA_DIR = os.path.join(BASE_DIR, 'data/processed/')
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data/all_hourly_data.h5')
PROCESSED_DATA_FILE_PATH = os.path.join(BASE_DIR, 'data/processed_data.h5')

FIG_DIR = os.path.join(BASE_DIR, 'figures/')
FIG_DEMOGRAPHICS_DIR = os.path.join(FIG_DIR, 'demographics/')
FIG_VITALS_LABS_DIR = os.path.join(FIG_DIR, 'vitals_labs/')
FIG_DIAGNOSES_DIR = os.path.join(FIG_DIR, 'diagnoses/')
FIG_INTERVENTIONS_DIR = os.path.join(FIG_DIR, 'interventions/')

PROCESSING_DIR = os.path.join(BASE_DIR, 'src/data_preprocessing/')

SCRIPTS_DIR = os.path.join(BASE_DIR, 'sql_queries')
SCRIPTS_VITAL_SIGNS_DIR = os.path.join(SCRIPTS_DIR, 'vital_signs/')
SCRIPTS_LAB_RESULTS_DIR = os.path.join(SCRIPTS_DIR, 'lab_results/')

GAP_TIME = 6  # In hours
WINDOW_SIZE = 24 # In hours
ID_COLS = ['subject_id', 'hadm_id', 'icustay_id']
TRAIN_FRAC, DEV_FRAC, TEST_FRAC = 0.7, 0.1, 0.2
SEED = 1
