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

''' 
Notes to self:

Need to implement dynamic token checking for RAG and split payload
requests in order to capture all user information. Change the JSON conversion from JS to python 
script to construct final output in backend


'''


OLLAMA_API_URL = "http://localhost:11434/api/generate"

class MedicalRecordGenerator():
    def __init__(self):
        self.model_name = "mistral"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def summarise_health_record(self, text_prompt, name):
        print(name," Summarisation in progress...")
        
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
        constructed_prompt = f'''
        Summarise **all** the patient's past and current medication in an organised manner.

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
        Ensure that the output is valid JSON. if there are no medications present return an empty list and no additional text or comments'''
        generator = MedicalRecordGenerator()
        summary = generator.summarise_health_record(constructed_prompt, 'medications')
        return JsonResponse({'success': True, 'summary': summary, 'RAG': medication_information})
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
        constructed_prompt = f''' Summarise **all** the patient's allergies in an organised manner.
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
        Ensure that the output is valid JSON, if there are no allergies present return an empty list and no additional text or comments
        '''
        generator = MedicalRecordGenerator()
        summary = generator.summarise_health_record(constructed_prompt, 'allergies')
        return JsonResponse({'success': True, 'summary': summary, 'RAG': allergy_information})
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
        constructed_prompt = f'''Summarise **all** the patient's past appointments and encounters in an organised manner.
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
        Ensure that the output is valid JSON. If there are no encounters present return an empty list and no additional text or comments'''
        generator = MedicalRecordGenerator()
        summary = generator.summarise_health_record(constructed_prompt, 'encounters')
        
        return JsonResponse({'success': True, 'summary': summary, 'RAG': encounter_information})
    
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False})
