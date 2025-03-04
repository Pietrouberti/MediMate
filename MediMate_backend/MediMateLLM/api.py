from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import torch
import requests
from API_KEYS import MediMate_API_KEY
from .prompt import prompt
from patients.models import Patients
from patients.serializers import PatientSerializer
from dataset_uploader.vector_database_indexer import rag_entry_point
from transformers import AutoModelForCausalLM, LlamaTokenizer
import torch

OLLAMA_API_URL = "http://localhost:11434/api/generate"

class MedicalRecordGenerator():
    def __init__(self):
        self.model_name = "mistral"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def summarise_health_record(self, text_prompt):
        print("OOP TEST", self.model_name, self.device)
        payload = {
            "model": self.model_name,
            "prompt": text_prompt,
            "stream": False,
        }
        
        try: 
            response = requests.post(OLLAMA_API_URL, json=payload)
            response_data = response.json()   
            return response_data.get("response", None)
        except Exception as e:
            return e


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_medication_records(request, id):
    try: 
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'medications')
        medication_information = results.get('medications', 'No Medications')
        print(medication_information)
        constructed_prompt = f'''
        Summarise the patient's past and current medication in an organised manner.

        Medication Information: 
        {medication_information}

        Please provide the result in the following JSON format without any additional text:
        {{
        "summary": "<Overall summary of the Medication>",
        "currentMedication": [
            {{
            "startDate": "<Medication Start date in YYYY/MM/DD format>",
            "details": "<Detailed description of the medication>"
            }}
            // You can list as many medications as necessary
        ],
        "oldMedication": [
            {{
                "startDate": "<Medication Start data in YYYY/MM/DD format>",
                "endDate": "<Medication End data in YYYY/MM/DD format>",
                "details": "<Detailed description of the medication>"
            }}
        ]
        }}
        Ensure that the output is valid JSON.'''
        generator = MedicalRecordGenerator()
        summary = generator.summarise_health_record(constructed_prompt)
        return JsonResponse({'success': True, 'summary': summary})
    except Exception as e:
        return JsonResponse({'error': e, 'success': False})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_allergy_records(request, id):
    try:
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'allergy')
        allergy_information = results.get('allergy', 'no allergies')
        constructed_prompt = f''' Summarise the patient's allergies in an organised manner.
        List the allergies in descending order (most recent last).
        
        Allergy Information:
        {allergy_information}
        
        Please provide the results in the following JSON format without any additional text:
        {{
            "summary": "<Overall summary of allergies>"
            "allergy": [
                {{
                    "date": "<Allergy Start date in YYYY/MM/DD>"
                    "details": "<Detailed description of the allergy>"
                }}
            ]
        }} 
        Ensure that the output is valid JSON
        '''
        generator = MedicalRecordGenerator()
        summary = generator.summarise_health_record(constructed_prompt)
        print(summary)
        return JsonResponse({'success': True, 'summary': summary})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_encounter_records(request, id):
    try: 
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'encounters')
        encounter_information = results.get('appointments', 'no appointments')
        print(encounter_information)
        constructed_prompt = f'''Summarise the patient's past appointments and encounters in an organised manner.
        List the encounters in descending order (most recent last).

        Encounter Information: 
        {encounter_information}

        Please provide the result in the following JSON format without any additional text:
        {{
        "summary": "<Overall summary of the encounters>",
        "encounters": [
            {{
            "date": "<Encounter date in YYYY/MM/DD format>",
            "details": "<Detailed description of the encounter>"
            }}
            // You can list as many encounters as necessary
        ]
        }}
        Ensure that the output is valid JSON.'''
        generator = MedicalRecordGenerator()
        summary = generator.summarise_health_record(constructed_prompt)
        
        return JsonResponse({'success': True, 'summary': summary})
    
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False})
