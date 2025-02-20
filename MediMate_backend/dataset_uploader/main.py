import pandas as pd
from datetime import datetime
from patients.models import Patients


def clean_patient_data(file_path):
    df = pd.read_csv(file_path)
    patient_columns_of_interest = {
        'Id': 'Id',
        'BIRTHDATE': 'BIRTHDATE',
        'DEATHDATE': 'DEATHDATE',
        'FIRSTNAME': 'FIRST',
        'LASTNAME': 'LAST',
        'GENDER': 'GENDER',
        'ETHNICITY': 'ETHNICITY',
    }

    df = df[list(patient_columns_of_interest.values())]
    df = df[df['DEATHDATE'].isna()]
    df = df.drop(columns=['DEATHDATE'])
    required_columns = ['Id', 'BIRTHDATE', 'FIRST', 'LAST', 'GENDER', 'ETHNICITY']
    df = df.dropna(subset=required_columns)
    df['BIRTHDATE'] = pd.to_datetime(df['BIRTHDATE'], errors='coerce')
    df = df.dropna(subset=['BIRTHDATE'])
    current_date = datetime.today()
    df['AGE'] = df['BIRTHDATE'].apply(lambda x: (current_date - x).days // 365)
    df = df.dropna(subset=['AGE'])
    
    return df

def load_patients_into_db(file_path):
    cleaned_df = clean_patient_data(file_path)
    
    patients = []
    for _, row in cleaned_df.iterrows():
        patient = Patients(
            id=row['Id'],
            first_name=row['FIRST'],
            last_name=row['LAST'],
            age=row['AGE'],
            date_of_birth=row['BIRTHDATE'].date(),
            gender=row['GENDER'],
            ethnicity=row['ETHNICITY'],
            address=""
        )
        patients.append(patient)
    
    Patients.objects.bulk_create(patients)

