# FuzzyMedNet: An Explainable Deep Learning Framework for Medical Diagnostics

## About

FuzzyMedNet is a comprehensive deep learning framework tailored for medical diagnostics, leveraging the strengths of Fuzzy Logic to bridge the gap between high predictive accuracy and model explainability. This repository is organized into the following directories:

- **Data**: This directory contains the dataset post-processing using [MIMIC-Extract](https://github.com/MLforHealth/MIMIC_Extract/tree/master) pipeline.
- **FuzzyModules**: Scripts and modules related to the integration of Fuzzy Logic.
- **Notebooks**: Jupyter Notebooks demonstrating the usage, training, and evaluation of the models.
- **Resources**: Contains supporting files, expected schema of output tables, and other pertinent documents.
- **Utils**: Scripts and tools that facilitate data preprocessing, model evaluation, and other utilities.

## Contextual Background

In the intersection of Artificial Intelligence (AI) and healthcare, the ability of models to make transparent decisions is of paramount importance. While Deep Learning (DL) has achieved remarkable feats in medical diagnostics, its 'black-box' nature poses challenges. FuzzyMedNet aims to address this by embedding Fuzzy Logic principles into DL models, enhancing their transparency and trustworthiness.

## Dataset

The project employs data from the [MIMIC-III](https://physionet.org/content/mimiciii/1.4/) dataset. For data pre-processing, the [MIMIC-Extract](https://github.com/MLforHealth/MIMIC_Extract/tree/master) pipeline was utilized.

## Using FuzzyMedNet

To get started with FuzzyMedNet, follow the steps below:

### Step 0: Prerequisites

Ensure your local system meets the following prerequisites:

#### Executables on the PATH:

`conda`<br>
`psql (PostgreSQL 9.4 or higher)`<br>
`git`<br>

#### Databases:

MIMIC-III psql relational database. If you haven't set this up, refer to the [MIT-LCP Repo](https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iii/buildmimic) for instructions.

#### Data Extraction:

Utilize the [/utils/Makefile](./utils/Makefile) to handle data extraction tasks.

### Step 1: Set Up the Environment

1. **Creating a Conda Environment**:
   - Use the provided `fuzzymednet_env_py36.yml` file to create a new conda environment:
     ```bash
     conda env create --force -f fuzzymednet_env_py36.yml
     ```

2. **Activating the Conda Environment**:
   - After creation, activate the environment using:
     ```bash
     conda activate fuzzymednet_env
     ```

3. **Installing Additional Packages**:
   - Some packages might need to be installed via pip. Use the provided `requirements.txt` file to ensure all necessary packages are installed:
     ```bash
     pip install -r requirements.txt
     ```