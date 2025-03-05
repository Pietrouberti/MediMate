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
import tiktoken
import json
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
        self.chunk_size = 400
        
    def split_prompt_text(self, rag_info):
        encoding = tiktoken.get_encoding("gpt2")
        tokens = encoding.encode(rag_info);
        prompt_chunks = []
        for i in range(0, len(tokens), self.chunk_size):
            chunk_token = tokens[i:i + self.chunk_size]
            chunk_text = encoding.decode(chunk_token)
            prompt_chunks.append(chunk_text)
        
        return prompt_chunks
        
    def summarise_health_record(self, text_prompt):
        print("Summarisation in progress...")
        
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

    def combine_summaries_as_json(self, summary_list, parentKey ,orderKey):
        json_list = []
        print("Response", summary_list)
        for s in summary_list:
            cleaned = s.replace("```json", "").replace("```", "").strip()
            json_list.append(json.loads(cleaned))

        combined = {"summary": "", parentKey: []}
        for obj in json_list:
            if combined["summary"]:
                combined["summary"] += " "
            combined["summary"] += obj["summary"]
            combined[parentKey].extend(obj[parentKey])

        combined[parentKey].sort(key=lambda x: x[orderKey])
        print(json.dumps(combined, indent=4))
        return combined

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_medication_records(request, id):
    try: 
        constructed_prompt_list = []
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'medications')
        medication_information = results.get('medications', 'No Medications')
        generator = MedicalRecordGenerator()
        chunked_info = generator.split_prompt_text(medication_information)
        for i in chunked_info:
            constructed_prompt = f'''
            Summarise **all** the patient's past and current medication in an organised manner.

            Medication Information: 
            {i}

            Please provide the result in the following JSON format without any additional text:
            {{
                "summary": "<Overall summary of the medications>",
                "medications": [
                    {{
                        "startDate": "<Medication Start date in YYYY/MM/DD format>",
                        "endDate": "<Medication End date in YYYY/MM/DD format>",
                        "details": "<Detailed description of the medication>"
                    }}
                ]
            }}
            Ensure that the output is valid JSON. if there are no medications present return an empty list and no additional text or comments'''
            constructed_prompt_list.append(constructed_prompt)
            
        print("constructed Prompts: \n \n ", constructed_prompt_list)
        for i in constructed_prompt_list:
            print("generating response: ", i, " package: \n ", i)   
            summary_responses.append(generator.summarise_health_record(i))
        
        summary = generator.combine_summaries_as_json(summary_responses, 'medications' ,'startDate')
        return JsonResponse({'success': True, 'summary': summary, 'RAG': medication_information})
    except Exception as e:
        return JsonResponse({'error': e, 'success': False})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_allergy_records(request, id):
    try:
        constructed_prompt_list = []
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'allergy')
        allergy_information = results.get('appointments', 'no allergies')
        generator = MedicalRecordGenerator()
        chunked_info = generator.split_prompt_text(allergy_information)
        for i in chunked_info:
            constructed_prompt = f''' Summarise **all** the patient's allergies in an organised manner.
            List the allergies in descending order (most recent last).
            
            Allergy Information:
            {i}
            
            Please provide the results in the following JSON format without any additional text:
            
            {{
                "summary": "<Overall summary of allergies>",
                "allergy": [
                    {{
                        "date": "<Allergy Start date in YYYY/MM/DD>",
                        "details": "<Detailed description of the allergy>"
                    }}
                ]
            }} 
            Ensure that the output is valid JSON, if there are no allergies present return an empty list and no additional text or comments
            '''
            constructed_prompt_list.append(constructed_prompt)
            
        print("constructed Prompts: \n \n ", constructed_prompt_list)
        for i in constructed_prompt_list:
            print("generating response: ", i, " package: \n ", i)   
            summary_responses.append(generator.summarise_health_record(i))
        
        summary = generator.combine_summaries_as_json(summary_responses, 'allergy' ,'date')
        return JsonResponse({'success': True, 'summary': summary, 'RAG': allergy_information})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_encounter_records(request, id):
    try: 
        constructed_prompt_list = []
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'encounters')
        encounter_information = results.get('appointments', 'no appointments')
        generator = MedicalRecordGenerator()
        chunked_info = generator.split_prompt_text(encounter_information)

        for i in chunked_info:
            constructed_prompt = f'''Summarise **all** the patient's past appointments and encounters in an organised manner.
            List the encounters in descending order (most recent last).

            Encounter Information: 
            {i}

            Please provide the result in the following JSON format without any additional text:
            {{
            "summary": "<Overall summary of the encounters>",
            "encounters": [
                {{
                    "date": "<Encounter date in YYYY/MM/DD format>",
                    "details": "<Detailed description of the encounter>"
                }}
            ]
            }}
            Ensure that the output is valid JSON. If there are no encounters present return an empty list and no additional text or comments'''
            
            constructed_prompt_list.append(constructed_prompt)
        
        print("constructed Prompts: \n \n ", constructed_prompt_list)
        for i in constructed_prompt_list:
            print("generating response: ", i, " package: \n ", i)   
            summary_responses.append(generator.summarise_health_record(i))
        
        summary = generator.combine_summaries_as_json(summary_responses, 'encounters' ,'date')
        return JsonResponse({'success': True, 'summary': summary, 'RAG': encounter_information})
    
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e), 'success': False})
