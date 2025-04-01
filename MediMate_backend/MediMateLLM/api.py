from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import torch
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from dataset_uploader.vector_database_indexer import rag_entry_point, get_patient_active_medication, extract_drug_names
import torch
import json
from datetime import datetime
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
from MediMate_backend.settings import model
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from rouge_score import rouge_scorer
from collections import Counter
import textstat
from bert_score import score


OLLAMA_API_URL = "http://localhost:11434/api/generate"


class SummaryEvaluationMetrics():
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
    
    def evaluate_summary(self, combined_summary, list_of_summaries):
        try:
            print("Summary Evaluation in progress")
            conciseness_metrics = self.conciseness_metric_calculator(combined_summary, list_of_summaries)
            coverage_metrics = self.coverage_metric_calculator(combined_summary, list_of_summaries)
            faithfulness_metrics = self.faithfulness_metric_calculator(combined_summary, list_of_summaries)
            redundancy_metrics = self.redundancy_metric_calculator(combined_summary)
            fluency_metrics = self.fluency_metric_calculator(combined_summary)
            
            return {
                "conciseness": conciseness_metrics,
                "coverage": coverage_metrics,
                "faithfulness": faithfulness_metrics,
                "redundancy": redundancy_metrics,
                "fluency": fluency_metrics,
            }
        except Exception as e:
            print(e)
            return {"error": str(e)}
    
    def conciseness_metric_calculator(self, combined_summary, list_of_summaries):
        print("Conciseness Evaluation in progress")
        compression_ratio = len(combined_summary) / sum([len(s) for s in list_of_summaries])
        sentences = sent_tokenize(combined_summary)
        avg_sentence_length = sum([len(s.split()) for s in sentences]) / len(sentences)
        words = word_tokenize(combined_summary)
        stopword_ratio = sum([1 for w in words if w in self.stop_words]) / len(words)
        
        return {
            "compression_ratio": compression_ratio,
            "avg_sentence_length": avg_sentence_length,
            "stopword_ratio": stopword_ratio
        }

    def coverage_metric_calculator(self, combined_summary, list_of_summaries):
        print("Coverage Evaluation in progress")
        text_ref = " ".join(list_of_summaries)
        scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        score = scorer.score(combined_summary, text_ref)
        return score['rougeL'].recall
    
    def faithfulness_metric_calculator(self, combined_summary, list_of_summaries):
        print("Faithfulness Evaluation in progress")
        embeddings = model.encode(list_of_summaries, convert_to_tensor=True)
        embeddings_combined = model.encode(combined_summary, convert_to_tensor=True)
        similarity_scores = util.cos_sim(embeddings_combined, embeddings).mean().item()
        return similarity_scores
    
    def redundancy_metric_calculator(self, combined_summary, n=3):
        print("Redundancy Evaluation in progress")
        tokens = word_tokenize(combined_summary.lower())
        n_grams = list(ngrams(tokens, n))
        counts = Counter(n_grams)
        repeated = sum(1 for count in counts.values() if count > 1)
        return repeated / len(n_grams)
    
    def fluency_metric_calculator(self, combined_summary):
        print("Fluency Evaluation in progress")
        fluency = textstat.flesch_reading_ease(combined_summary)
        return fluency
    
    
'''MedicalPrescriptionDector class: Contains finetuned BERT model for detecting drug-drug interactions in between a patients active medication and a new prescription
    verify_medical_prescription: Queries the model to determine the severity of the interaction between the active medication and the new prescription'''
class MedicalPrescriptionDetector():
    def __init__(self):
        self.model = "A:/Dissertation/MediMate/fine_tuned_ddi_BERT1_model"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model)
        self.pipeline = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
    
    def verify_medical_prescription(self, active_medication , prescription):
        results = []
        for i in active_medication:
            input_text = (
                f"{i} + {prescription}"
            )
            result = self.pipeline(input_text)
            severity_options = {'Minor': 'LABEL_0', 'Moderate': 'LABEL_2', 'Major': 'LABEL_1', 'Unknown': 'LABEL_3'} 
            for severity, label in severity_options.items():
                if result[0]['label'] == label:
                    result[0]['severity'] = severity
                    break
            result[0].update({'active_medication': i, 'prescription': prescription})
            print(result)
            results.append(result)
        return results 

'''MedicalDiagnosisChecker class: Contains finetuned BERT model for verifying a medical diagnosis based on patient information, symptoms, diagnosis notes and proposed diagnosis
    verify_medical_diagnosis: Queries the model to determine the validity of the proposed diagnosis based on the patient information'''
class MedicalDiagnosisChecker():
    def __init__(self):
        self.model = "A:/Dissertation/MediMate/fine-tuned-ClinicalBERT-diagnosis-verifier"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model)
        self.pipeline = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
    
    def verify_medical_diagnosis(self, patient_data ,diagnosis_notes, symptoms, diagnosis):
        input_text = (
            f"Patient Info: {patient_data}\n"
            f"Symptoms: {symptoms}\n"
            f"Doctor's Notes: Observations: {diagnosis_notes}\n"
            f"Proposed Diagnosis: {diagnosis}"
        )
        
        print(input_text)
        
        result = self.pipeline(input_text)
        return result
        

'''MedicalSummaryRecordGenerator class: contains logic to chunk RAG data and Mistral model to generate summarisations based of patient Electornic Health Records '''
'''split_prompt_text: splits the RAG data into chunks of text that are suitable for the LLM model to process'''
'''summarise_health_record: queries the LLM model to generate a summary based on the chunked RAG data'''
'''combine_summaries_as_json: combines the LLM response into a json format (deprecated as summarisations are combined using divide and conquer)'''
'''format_date: formats the date string into a readable format for JSON response'''
'''structure_raw_medication_data_as_json: structures the raw medication data into a json format for JSON response'''
'''structure_raw_allergy_data_as_json: structures the raw allergy data into a json format for JSON response'''
'''structure_raw_appointment_data_as_json: structures the raw appointment data into a json format for JSON response'''
'''structure_raw_condition_data_as_json: structures the raw condition data into a json format for JSON response'''
class MedicalSummaryRecordGenerator():
    def __init__(self):
        self.model = "llama3.1"
        self.max_chunk_size = 800 
    
    # splits retrived formated patient record data into specificly size chunks of data
    # returns a list of ready to process data chunks  
    def split_prompt_text(self, rag_info):
        items = rag_info.split('|')
        prompt_chunks = []
        current_chunk = ""

        for item in items:
            if len(current_chunk) + len(item) + 1 > self.max_chunk_size:
                prompt_chunks.append(current_chunk.strip())
                current_chunk = item + "|"
            else:
                current_chunk += item + "|"

        if current_chunk:
            prompt_chunks.append(current_chunk.strip())

        return prompt_chunks
    
    def summarise_health_record(self, text_prompt):
        print("Summarisation in progress...")
        
        payload = {
            "model": self.model,
            "prompt": text_prompt,
            "stream": False,
        }
        
        
        try: 
            response = requests.post(OLLAMA_API_URL, json=payload)
            response_data = response.json()   
            return response_data.get("response", None)
        except Exception as e:
            return e

    # Deprecated (Not used anymore due to shift to divide and conquer summarisation)
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


    def format_date(self, date_str):
        try: 
            return datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception as e:
            return "<not specified>"

    def structure_raw_medication_data_as_json(self, raw_data):
        result = []
        for row in raw_data:
            start_date = self.format_date(row.get("START", "<not specified>"))
            end_date = self.format_date(row.get("STOP", "<not specified>"))
            description = row.get("DESCRIPTION", "<not specified>").strip()
            reason = row.get("REASONDESCRIPTION", "").strip()
            dispenses = int(row.get("DISPENSES", "<not specified>"))
            detail = f"{description} for {reason}"
            if dispenses > 1:
                detail += f" (Dispensed: {dispenses} times)"
            
            result.append({
                "startDate": start_date,
                "endDate": end_date,
                "details": detail
            })
        return result
    
    def structure_raw_allergy_data_as_json(self, raw_data):
        result = []
        print(raw_data)
        for row in raw_data:
            start_date = self.format_date(row.get("START", "<not specified>"))
            allergen = row.get("DESCRIPTION", "<not specified>").strip()
            category = row.get("CATEGORY", "<not specified>").strip()

            reactions = []
            if row.get("REACTION1"):
                desc1 = row.get("DESCRIPTION1", "").strip()
                severity1 = row.get("SEVERITY1", "").strip()
                reactions.append(f"{desc1} --> Severity: {severity1}" if severity1 else desc1)
            
            if row.get("REACTION2"):
                desc2 = row.get("DESCRIPTION2", "").strip()
                severity2 = row.get("SEVERITY2", "").strip()
                reactions.append(f"{desc2} --> Severity: {severity2}" if severity2 else desc2)

            detail = f"Allergy to {allergen} ({category})"
            if reactions:
                detail += f" | Reactions: {', '.join(reactions)}"

            result.append({
                "startDate": start_date,
                "details": detail
            })
        
        return result
    
    def structure_raw_appointment_data_as_json(self, raw_data):
        result = []
        for row in raw_data:
            start_date = self.format_date(row.get("START", "<not specified>"))
            description = row.get("DESCRIPTION", "<not specified>").strip()
            reason = row.get("REASONDESCRIPTION", "").strip()
            result.append({
                "startDate": start_date,
                "details": f"{description} - {reason}"
            })
        return result
    
    def structure_raw_condition_data_as_json(self, raw_data):
        result = []
        for row in raw_data:
            start_date = self.format_date(row.get("START", "<not specified>"))
            end_date = self.format_date(row.get("STOP", "<not specified>"))
            description = row.get("DESCRIPTION", "<not specified>").strip()
            result.append({
                "startDate": start_date,
                "endDate": end_date,
                "details": description
            })
        return result


'''divide_and_conquer_summarization: Recursively combines the summaries generated by the LLM model using a divide and conquer approach, 
to ensure that the final summary is consice and readable (switch was made due to the frequency of hallucinations when combining all summaries at once)'''            
def divide_and_conquer_summarization(generator, summaries):
    if len(summaries) == 1:
        return summaries[0]
    
    merged_summaries = []
    
    for i in range(0, len(summaries), 2):
        if i + 1 < len(summaries):
            print(f"Divide and Conquer Summarisation for index {i} and {i+1}")
            combined = generator.summarise_health_record(
                f"""
                Combine the following summaries into a clear, structured paragraph. 
                Ensure all key information is captured in final summary. Avoid dense phrasing and repetition. Prioritize clarity and coverage. 
                Output only the final summary with no additional text:
                1. {summaries[i]}
                2. {summaries[i+1]}"""
            )
            merged_summaries.append(combined)
        else:
            print(f"Reached the end of the summary list {i}")
            merged_summaries.append(summaries[i])

    return divide_and_conquer_summarization(generator, merged_summaries)



'''get_medication_records: end point for patient medication summary'''
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_medication_records(request, id, metrics):
    try: 
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'medications')
        medication_information = results.get('medications_formatted', 'No Medications')
        medication_raw = results.get('medications_raw', 'No Medications')
        generator = MedicalSummaryRecordGenerator()
        chunked_info = generator.split_prompt_text(medication_information)
        json_list_of_medication_data = generator.structure_raw_medication_data_as_json(medication_raw)
        for i in chunked_info:
            if i == '|':
                i = 'No Medications'
            constructed_prompt = f'''
            You are a summarization model. You will be given a chunk of text that contains information about a patient's medication records. You are required to summarize the all information in a concise and readable manner. If no text is provided please respond with "No Medications" and don't include any additional text before or after summarization.
            Medication Information: 
            {i} '''
            if(len(chunked_info) > 1):
                print(f'Generating Summary for chunk {chunked_info.index(i) + 1}/{len(chunked_info)}')
            summary_responses.append(generator.summarise_health_record(constructed_prompt))
            
        summary = {"medications": json_list_of_medication_data, "summary": ""}
        summary['summary'] = divide_and_conquer_summarization(generator, summary_responses)
        
        if (metrics.lower() == 'true'):
            evaluation_metrics = SummaryEvaluationMetrics()
            evaluation_results = evaluation_metrics.evaluate_summary(summary['summary'], summary_responses)
            return JsonResponse({'success': True, 'summary': summary, 'RAG': medication_information, 'evaluation': evaluation_results})
        else: 
            return JsonResponse({'success': True, 'summary': summary, 'RAG': medication_information})
    except Exception as e:
        return JsonResponse({'error': e, 'success': False})


'''get_allergy_records: end point for patient allergy summary'''
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_allergy_records(request, id, metrics):
    try:
        summary_responses = []
        patient_id = str(id) # converts patient id to str for vector db query
        results = rag_entry_point(patient_id, '', 'allergy') # retrives patient information from vector db 
        allergy_information = results.get('allergy_formatted', 'no Allergies')
        allergy_raw = results.get('allergy_raw', 'no Allergies')
        print(allergy_information)
        generator = MedicalSummaryRecordGenerator() # initiate the MedicalSummaryRecordGenerator class
        chunked_info = generator.split_prompt_text(allergy_information) # splits the retrived information into suitable token sizes
        json_list_of_allergy_data = generator.structure_raw_allergy_data_as_json(allergy_raw)
        print("ahh",allergy_information)
        for i in chunked_info: # loops through each chunk and adds it to query
            if i == '|':
                i = 'No Allergens'
            constructed_prompt = f'''
            You are a summarization model. You will be given a chunk of text that contains information about a patient's allergen records. You are required to summarize the all information in a concise and readable manner. If no text is provided please respond with "No Allergies" and don't include any additional text before or after summarization.            
            Allergen Information: 
            {i} '''
            if(len(chunked_info) > 1):
                print(f'Generating Summary for chunk {chunked_info.index(i) + 1}/{len(chunked_info)}')
            summary_responses.append(generator.summarise_health_record(constructed_prompt))# collects all the constructed queries 
            
        summary = {"allergy": json_list_of_allergy_data, "summary": ""}
        summary['summary'] = divide_and_conquer_summarization(generator, summary_responses)
        if (metrics.lower() == 'true'):
            evaluation_metrics = SummaryEvaluationMetrics()
            evaluation_results = evaluation_metrics.evaluate_summary(summary['summary'], summary_responses)
            return JsonResponse({'success': True, 'summary': summary, 'RAG': allergy_information, 'evaluation': evaluation_results})
        else: 
            return JsonResponse({'success': True, 'summary': summary, 'RAG': allergy_information})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e}) # pass error to frontend if something fails


'''get_encounter_records: end point for patient encounter summary'''
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_encounter_records(request, id, metrics):
    try: 
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'encounters')
        encounter_information = results.get('appointments_formatted', 'no appointments')
        encounter_raw = results.get('appointments_raw', 'no appointments')
        generator = MedicalSummaryRecordGenerator()
        json_list_of_encounter_data = generator.structure_raw_appointment_data_as_json(encounter_raw)
        chunked_info = generator.split_prompt_text(encounter_information)

        for i in chunked_info:
            if i == '|':
                i = 'No Appointments'
            constructed_prompt = f'''
                You are a summarization model. You will be given a chunk of text that contains information about a patient's appointment records. You are required to summarize the all information in a concise and readable manner. If no text is provided please respond with "No Appointments" and don't include any additional text before or after summarization.
                Appointment Information: 
                {i} '''
            
            if(len(chunked_info) > 1):
                print(f'Generating Summary for chunk {chunked_info.index(i) + 1}/{len(chunked_info)}')
            chunk_summary = generator.summarise_health_record(constructed_prompt)
            summary_responses.append(chunk_summary)
        
        summary = {"encounters": json_list_of_encounter_data, "summary": ""}
        summary['summary'] = divide_and_conquer_summarization(generator, summary_responses)
        if (metrics.lower() == 'true'):
            evaluation_metrics = SummaryEvaluationMetrics()
            evaluation_results = evaluation_metrics.evaluate_summary(summary['summary'], summary_responses)
            return JsonResponse({'success': True, 'summary': summary, 'RAG': encounter_information, 'evaluation': evaluation_results})
        else: 
            return JsonResponse({'success': True, 'summary': summary, 'RAG': encounter_information})
    
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False})


'''get_condition_records: end point for patient condition summary'''
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_condition_records(request, id, metrics):
    try:    
        summary_responses = []
        patient_id = str(id)
        results = rag_entry_point(patient_id, '', 'conditions')
        condition_information = results.get('conditions_formatted', 'no conditions')
        condition_raw = results.get('conditions_raw', 'no conditions')
        generator = MedicalSummaryRecordGenerator()
        json_list_of_condition_data = generator.structure_raw_condition_data_as_json(condition_raw)
        chunked_info = generator.split_prompt_text(condition_information)
        for i in chunked_info:
            if i == '|':
                i = 'No Conditions'
            constructed_prompt = f'''
                You are a summarization model. You will be given a chunk of text that contains information about a patient's condition records. You are required to summarize the all information in a concise and readable manner. If no text is provided please respond with "No Conditions" and don't include any additional text before or after summarization.
                Condition Information: 
                {i} '''
            if(len(chunked_info) > 1):
                print(f'Generating Summary for chunk {chunked_info.index(i) + 1}/{len(chunked_info)}')
            summary_responses.append(generator.summarise_health_record(constructed_prompt))
                
        summary = {"conditions": json_list_of_condition_data, "summary": ""}
        summary['summary'] = divide_and_conquer_summarization(generator, summary_responses)
        if (metrics.lower() == 'true'):
            evaluation_metrics = SummaryEvaluationMetrics()
            evaluation_results = evaluation_metrics.evaluate_summary(summary['summary'], summary_responses)
            return JsonResponse({'success': True, 'summary': summary, 'RAG': condition_information, 'evaluation': evaluation_results})
        else: 
            return JsonResponse({'success': True, 'summary': summary, 'RAG': condition_information})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e), 'success': False})

'''check_doctors_diagnosis: end point for checking the validity of a doctors diagnosis'''
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_doctors_diagnosis(request):
    patient_information = str(request.data['patient'])
    symptoms = str(request.data['symptoms'])
    diagnosis = str(request.data['diagnosis'])
    notes = str(request.data['notes'])
    
    try: 
        diagnosisChecker = MedicalDiagnosisChecker() 
        result = diagnosisChecker.verify_medical_diagnosis(patient_information, notes, symptoms, diagnosis)
        return JsonResponse({'success': True, 'result': result})
    except Exception as e: 
        return JsonResponse({'success': False, 'error': e})
    
'''check_medical_prescription: end point for checking the validity of a medical prescription'''
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_medical_prescription(request):
    try: 
        
        patient_id = str(request.data['patient'])
        prescription = str(request.data['prescription'])
        active_medication = get_patient_active_medication(patient_id)
        if len(active_medication) == 0:
            return JsonResponse({'success': True, 'result': ['Patient has no active medications']})
        else:     
            extracted_drug_name = extract_drug_names(active_medication)
            prescription_clash_detector = MedicalPrescriptionDetector()
            results = prescription_clash_detector.verify_medical_prescription(extracted_drug_name, prescription)
            return JsonResponse({'success': True, 'result': results})   
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})    
    