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

VITALS_AND_LABS = ['alanine aminotransferase',
                   'albumin',
                   'albumin ascites',
                   'albumin pleural',
                   'albumin urine',
                   'alkaline phosphate',
                   'anion gap',
                   'asparate aminotransferase',
                   'basophils',
                   'bicarbonate',
                   'bilirubin',
                   'blood urea nitrogen',
                   'co2',
                   'co2 (etco2, pco2, etc.)',
                   'calcium',
                   'calcium ionized',
                   'calcium urine',
                   'cardiac index',
                   'cardiac output thermodilution',
                   'cardiac output fick',
                   'central venous pressure',
                   'chloride',
                   'chloride urine',
                   'cholesterol',
                   'cholesterol hdl',
                   'cholesterol ldl',
                   'creatinine',
                   'creatinine ascites',
                   'creatinine body fluid',
                   'creatinine pleural',
                   'creatinine urine',
                   'diastolic blood pressure',
                   'eosinophils',
                   'fibrinogen',
                   'fraction inspired oxygen',
                   'fraction inspired oxygen set',
                   'glascow coma scale total',
                   'glucose',
                   'heart rate',
                   'height',
                   'hematocrit',
                   'hemoglobin',
                   'lactate',
                   'lactate dehydrogenase',
                   'lactate dehydrogenase pleural',
                   'lactic acid',
                   'lymphocytes',
                   'lymphocytes ascites',
                   'lymphocytes atypical',
                   'lymphocytes atypical csl',
                   'lymphocytes body fluid',
                   'lymphocytes percent',
                   'lymphocytes pleural',
                   'magnesium',
                   'mean blood pressure',
                   'mean corpuscular hemoglobin',
                   'mean corpuscular hemoglobin concentration',
                   'mean corpuscular volume',
                   'monocytes',
                   'monocytes csl',
                   'neutrophils',
                   'oxygen saturation',
                   'partial pressure of carbon dioxide',
                   'partial pressure of oxygen',
                   'partial thromboplastin time',
                   'peak inspiratory pressure',
                   'phosphate',
                   'phosphorous',
                   'plateau pressure',
                   'platelets',
                   'positive end-expiratory pressure',
                   'positive end-expiratory pressure set',
                   'post void residual',
                   'potassium',
                   'potassium serum',
                   'prothrombin time inr',
                   'prothrombin time pt',
                   'pulmonary artery pressure mean',
                   'pulmonary artery pressure systolic',
                   'pulmonary capillary wedge pressure',
                   'red blood cell count',
                   'red blood cell count csf',
                   'red blood cell count ascites',
                   'red blood cell count pleural',
                   'red blood cell count urine',
                   'respiratory rate',
                   'respiratory rate set',
                   'sodium',
                   'systemic vascular resistance',
                   'systolic blood pressure',
                   'temperature',
                   'tidal volume observed',
                   'tidal volume set',
                   'tidal volume spontaneous',
                   'total protein',
                   'total protein urine',
                   'troponin-i',
                   'troponin-t',
                   'venous pvo2',
                   'weight',
                   'white blood cell count',
                   'white blood cell count urine',
                   'ph',
                   'ph urine']

VITAL_SIGNS = vital_signs = [
    'heart rate',
    'respiratory rate',
    'systolic blood pressure',
    'diastolic blood pressure',
    'mean blood pressure',
    'temperature',
    'oxygen saturation',
    'fraction inspired oxygen',
    'glascow coma scale total',
    'pulmonary artery pressure mean',
    'pulmonary artery pressure systolic',
    'pulmonary capillary wedge pressure',
    'positive end-expiratory pressure',
    'peak inspiratory pressure',
    'plateau pressure',
    'respiratory rate set',
    'tidal volume observed',
    'tidal volume set',
    'tidal volume spontaneous',
    'weight',
    'height',
    'co2 (etco2, pco2, etc.)',
    'fraction inspired oxygen set',
    'positive end-expiratory pressure set',
    'systemic vascular resistance',
    'ph'
]

LAB_MEASUREMENTS = [item for item in VITALS_AND_LABS if item not in VITAL_SIGNS]