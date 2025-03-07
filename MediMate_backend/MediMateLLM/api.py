from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import torch
import requests
from dataset_uploader.vector_database_indexer import rag_entry_point
import torch
import tiktoken
import json


OLLAMA_API_URL = "http://localhost:11434/api/generate"


# MedicalRecordGenerator class used for querying LLM 
class MedicalRecordGenerator():
    def __init__(self):
        self.model_name = "mistral" # defines model to be used
        self.device = "cuda" if torch.cuda.is_available() else "cpu" # this is redundant code but if I make a switch to hugging face I have included it
        self.chunk_size = 800 # defines a maximum rag information token size in order to prevent passing an excess amount of tokens to LLM
     
    # splits the retrived data into chunks of data such that it doesn't exceed the chunk_size limit    
    def split_prompt_text(self, rag_info):
        items = rag_info.split('|')
        prompt_chunks = []
        current_chunk = ""

        for item in items:
            if len(current_chunk) + len(item) + 1 > self.chunk_size:
                prompt_chunks.append(current_chunk.strip())
                current_chunk = item + "|"
            else:
                current_chunk += item + "|"

        if current_chunk:
            prompt_chunks.append(current_chunk.strip())

        return prompt_chunks
    
    # Querys LLM through Ollama endpoint
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

    # takes the LLM `json` text response and converts it into an actual json format
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



# end point for patient medication summary
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
        summary['summary'] = generator.summarise_health_record('Summaries this text with no additional text or comments: ' + summary['summary'])
        return JsonResponse({'success': True, 'summary': summary, 'RAG': medication_information})
    except Exception as e:
        return JsonResponse({'error': e, 'success': False})


# end point for patient allergy summary
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_allergy_records(request, id):
    try:
        constructed_prompt_list = []
        summary_responses = []
        patient_id = str(id) # converts patient id to str for vector db query
        results = rag_entry_point(patient_id, '', 'allergy') # retrives patient information from vector db 
        allergy_information = results.get('allergy', 'no allergies')
        generator = MedicalRecordGenerator() # initiate the MedicalRecordGenerator class
        chunked_info = generator.split_prompt_text(allergy_information) # splits the retrived information into suitable token sizes
        for i in chunked_info: # loops through each chunk and adds it to query
            constructed_prompt = f''' 
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
            constructed_prompt_list.append(constructed_prompt) # collects all the constructed queries 
            
        print("constructed Prompts: \n \n ", constructed_prompt_list)
        for i in constructed_prompt_list: # loops through each constructed query and requests LLM for response
            print("generating response: ", i, " package: \n ", i)   
            summary_responses.append(generator.summarise_health_record(i))
        
        summary = generator.combine_summaries_as_json(summary_responses, 'allergy' ,'date') # converts LLM response into JSON for frontend managment
        summary['summary'] = generator.summarise_health_record('Summaries this text with no additional text or comments: ' + summary['summary']) # summaries the concatenated summaries improving summary clarity 
        return JsonResponse({'success': True, 'summary': summary, 'RAG': allergy_information})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e}) # pass error to frontend if something fails


# end point for encounter allergy summary
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
        summary['summary'] = generator.summarise_health_record('Summaries this text with no additional text or comments: ' + summary['summary'])
        return JsonResponse({'success': True, 'summary': summary, 'RAG': encounter_information})
    
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e), 'success': False})

# end point for condition allergy summary
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_condition_records(request, id):
    try:    
        constructed_prompt_list = []
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'conditions')
        condition_information = results.get('conditions', 'no conditions')
        generator = MedicalRecordGenerator()
        chunked_info = generator.split_prompt_text(condition_information)
        
        for i in chunked_info:
            constructed_prompt = f'''Summarise **all** the patient's conditions in an organised manner.
                List the conditions in descending order (most recent last).

                Patient Condition Information: 
                {i}

                Please provide the result in the following JSON format without any additional text:
                {{
                "summary": "<Overall summary of the conditions>",
                "conditions": [
                    {{
                        "startDate": "<condition Start date in YYYY/MM/DD format>",
                        "endDate": "<condition End date in YYYY/MM/DD format>",
                        "details": "<Detailed description of the condition>"
                    }}
                ]
                }}
                Ensure that the output is valid JSON. If there are no conditions present return an empty list and no additional text or comments'''
            constructed_prompt_list.append(constructed_prompt)
        
        print("constructed Prompts: \n \n ", constructed_prompt_list)
        for i in constructed_prompt_list:
            print("generating response: ", i)
            summary_responses.append(generator.summarise_health_record(i))
        
        summary = generator.combine_summaries_as_json(summary_responses, 'conditions', 'startDate')
        summary['summary'] = generator.summarise_health_record('Summaries this text with no additional text or comments: ' + summary['summary'])
        return JsonResponse({'success': True, 'summary': summary, 'RAG': condition_information})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e), 'success': False})