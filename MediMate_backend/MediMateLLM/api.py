from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import torch
import requests
from API_KEYS import MediMate_API_KEY
from dataset_uploader.vector_database_indexer import rag_entry_point
from transformers import AutoModelForCausalLM, LlamaTokenizer
import torch

OLLAMA_API_URL = "http://localhost:11434/api/generate"

class MedicalRecordGenerator():
    def __init__(self):
        self.model_name = "phi4"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def summarise_health_record(self, text_prompt):
        print("OOP TEST", self.model_name, self.device)
        payload = {
            "model": self.model_name,
            "prompt": text_prompt,
            "stream": False,
            "device": self.device
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
def medi_mate_llm_chat_entry_point(request, id):
    try: 
        patient_id = str(id)
        print(patient_id)
        results = rag_entry_point(patient_id, '')
        results_keys = ['allergy', 'conditions', 'medications', 'appointments']
        if not results or not all(key in results for key in results_keys):
            return JsonResponse({'error': 'Missing or malformed RAG results', 'success': False})
        text_prompt = f'''
        Patient Medical Record Summary:

        Allergies: {results.get('allergy', 'None reported')}
        Past Conditions: {results.get('conditions', 'None reported')}
        Past Medications: {results.get('medications', 'None reported')}
        Past Appointments: {results.get('appointments', 'None reported')}

        Please generate a concise yet informative summary of this patient's medical history.
        
        Split the summary into Allergy, Condition, Medications, Appointment subheadings and list the section summary items in order of STOP date
        '''
        print(text_prompt)

        medical_record_generator = MedicalRecordGenerator()
        summary = medical_record_generator.summarise_health_record(text_prompt)
        
        return JsonResponse({'success': True, 'summary': summary})
    
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False})
