import pandas as pd 
import chromadb 
from sentence_transformers import SentenceTransformer
from MediMate_backend.settings import model, chroma_client, allergy_collection, encounter_collection, condition_collection, medication_collection

'''

Notes to self: 

Need to create helper function to effectivly wrangle the data to ensure no null values in indexable columns.
Load in 1000 patient dataset by executing file with load_dataset() as entry point


'''

def load_dataset():
    allergies_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/allergies.csv')
    conditions_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/conditions.csv')
    encounters_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/encounters.csv')
    medications_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/medications.csv')
    
    index_allergy_data(allergies_dataset)
    index_conditions_data(conditions_dataset)
    index_encounters_data(encounters_dataset)
    index_medications_data(medications_dataset)


def generate_embeddings(df, embedding_columns):
    df['index_text'] = df[embedding_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    embeddings = model.encode(df['index_text'].tolist(), show_progress_bar=True)
    return df, embeddings

def index_allergy_data(df):
    df, allergy_embeddings = generate_embeddings(df, ['DESCRIPTION', 'TYPE', 'CATEGORY', 'REACTION1', 'DESCRIPTION1', 'REACTION2', 'DESCRIPTION2'])
    for i, row in df.iterrows():
        allergy_collection.add(
            ids=[str(i)],
            embeddings=[allergy_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )
    
def index_conditions_data(df):
    df, conditions_embeddings = generate_embeddings(df, ['DESCRIPTION'])
    for i, row in df.iterrows():
        condition_collection.add(
            ids=[str(i)],
            embeddings=[conditions_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

def index_encounters_data(df):
    df, encounters_embeddings = generate_embeddings(df, ['ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION'])
    for i, row in df.iterrows():
        encounter_collection.add(
            ids=[str(i)],
            embeddings=[encounters_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

def index_medications_data(df):
    df, medications_embeddings = generate_embeddings(df, ['DESCRIPTION', 'REASONDESCRIPTION'])
    for i, row in df.iterrows():
        medication_collection.add(
            ids=[str(i)],
            embeddings=[medications_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

def rag_entry_point(patient_id, query_text, params):
    patient_electronic_health_record = {}
    allergy_important_keys = ['CATEGORY', 'CODE', 'SYSTEM', 'DESCRIPTION', 'DESCRIPTION1', 'START', 'STOP' 'SEVERITY1', 'REACTION1', 'SEVERITY2', 'REACTION2']
    conditions_important_keys = ['START', 'STOP', 'DESCRIPTION', 'SYSTEM', 'CODE']
    medications_important_keys = ['START', 'STOP', 'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION', 'DISPENSES']
    encounters_important_keys = ['START', 'STOP', 'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION']
    # get patient specific information from datasets
    if params == 'allergy':
        allergy_results = patient_record_collector(patient_id, allergy_collection)
        patient_electronic_health_record['allergy'] = format_dataset_record(allergy_results, allergy_important_keys)
        return patient_electronic_health_record
    if params == 'conditions':
        conditions_results = patient_record_collector(patient_id, condition_collection)
        patient_electronic_health_record['conditions'] = format_dataset_record(conditions_results, conditions_important_keys)
        return patient_electronic_health_record
    if params == 'medications': 
        medications_results = patient_record_collector(patient_id, medication_collection)
        patient_electronic_health_record['medications'] = format_dataset_record(medications_results, medications_important_keys)
        return patient_electronic_health_record
    if params == 'encounters':
        encounters_results = patient_record_collector(patient_id, encounter_collection)
        patient_electronic_health_record['appointments'] = format_dataset_record(encounters_results, encounters_important_keys)
        return patient_electronic_health_record
    else: 
        
        allergy_results = patient_record_collector(patient_id, allergy_collection)
        conditions_results = patient_record_collector(patient_id, condition_collection)
        medications_results = patient_record_collector(patient_id, medication_collection)
        encounters_results = patient_record_collector(patient_id, encounter_collection)
               
        patient_electronic_health_record['allergy'] = format_dataset_record(allergy_results, allergy_important_keys)
        patient_electronic_health_record['conditions'] = format_dataset_record(conditions_results, conditions_important_keys)
        patient_electronic_health_record['medications'] = format_dataset_record(medications_results, medications_important_keys)
        patient_electronic_health_record['appointments'] = format_dataset_record(encounters_results, encounters_important_keys)
        
        return patient_electronic_health_record
    

    
def format_dataset_record(retrieval_results, keys):
    formatted_records = []
    for record in retrieval_results:
        parts = [f"{key}: {record[key]}" for key in keys if key in record and record[key] not in (None, 'null')]
        formatted_records.append(", ".join(parts))
    return " | ".join(formatted_records)


def patient_record_collector(patient_id, collection_obj):
     results = collection_obj.get(where={"PATIENT": patient_id})
     metadatas = results.get('metadatas', [])
     return metadatas

def similar_record_context_search(query_text, collection_obj, top_k=2):
    query_embedding = model.encode([query_text]).tolist()
    results = collection_obj.query(
        query_embeddings = query_embedding,
        n_results = top_k,
        include = ["documents", "metadatas", "distances"]
    )
    return results
    
