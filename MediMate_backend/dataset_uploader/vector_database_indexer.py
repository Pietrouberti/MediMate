import pandas as pd 
import chromadb 
import os
from sentence_transformers import SentenceTransformer
from MediMate_backend.settings import model, allergy_collection, encounter_collection, condition_collection, medication_collection, drug_interaction_collection

# Entry point for initialisation of vector database, it loads the CSV files and executes seperate indexing functions
def load_dataset():
    allergies_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/allergies.csv')
    conditions_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/conditions.csv')
    encounters_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/encounters.csv')
    medications_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/medications.csv')
    drug_interaction_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/filtered_drug_interactions.csv')
    
    index_drug_interaction_data(drug_interaction_dataset)
    index_allergy_data(allergies_dataset)
    index_conditions_data(conditions_dataset)
    index_encounters_data(encounters_dataset)
    index_medications_data(medications_dataset)

def index_single_record(df, collection, id, important_columns):
    print(df)
    df, embeddings = generate_embeddings(df, important_columns)

    collection.add(
        ids=[str(id)],
        embeddings=[embeddings[0].tolist()],
        documents=[df['index_text'].iloc[0]],  # FIXED: extract string
        metadatas=[df.to_dict(orient='records')[0]]  # also make sure metadata is a dict, not Series
    )


# generates embeddings for vector db
def generate_embeddings(df, embedding_columns):
    df['index_text'] = df[embedding_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    embeddings = model.encode(df['index_text'].tolist(), show_progress_bar=True)
    return df, embeddings


def index_drug_interaction_data(df):
    df, drug_interaction_embeddings = generate_embeddings(df, ['Drug_A','Drug_B','Level'])
    for i, row in df.iterrows():
        drug_interaction_collection.add(
            ids=[str(i)],
            embeddings=[drug_interaction_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )
        print('indexing', i)

# indexes allergy data by adding embedding to the specific vector db collection
def index_allergy_data(df):
    df, allergy_embeddings = generate_embeddings(df, ['DESCRIPTION', 'TYPE', 'CATEGORY', 'REACTION1', 'DESCRIPTION1', 'REACTION2', 'DESCRIPTION2'])
    for i, row in df.iterrows():
        allergy_collection.add(
            ids=[str(i)],
            embeddings=[allergy_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

# indexes conditions data by adding embedding to the specific vector db collection
def index_conditions_data(df):
    df, conditions_embeddings = generate_embeddings(df, ['DESCRIPTION'])
    for i, row in df.iterrows():
        condition_collection.add(
            ids=[str(i)],
            embeddings=[conditions_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

# indexes encounters data by adding embedding to the specific vector db collection
def index_encounters_data(df):
    df, encounters_embeddings = generate_embeddings(df, ['ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION'])
    for i, row in df.iterrows():
        encounter_collection.add(
            ids=[str(i)],
            embeddings=[encounters_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

# indexes medications data by adding embedding to the specific vector db collection
def index_medications_data(df):
    df, medications_embeddings = generate_embeddings(df, ['DESCRIPTION', 'REASONDESCRIPTION'])
    for i, row in df.iterrows():
        medication_collection.add(
            ids=[str(i)],
            embeddings=[medications_embeddings[i].tolist()],
            documents=[row['index_text']],
            metadatas=[row.to_dict()]
        )

# note to self: ustalise the query text parameter to permit doctor to fetch similar records
# entry point for dynamic patient data retrival, it fetches all relevant patient information, and once implemented will search DB for similar cases using query_text param
def rag_entry_point(patient_id, query_text, params):
    patient_electronic_health_record = {}
    allergy_important_keys = ['CATEGORY', 'CODE', 'SYSTEM', 'DESCRIPTION', 'DESCRIPTION1', 'START', 'STOP' 'SEVERITY1', 'REACTION1', 'SEVERITY2', 'REACTION2']
    conditions_important_keys = ['START', 'STOP', 'DESCRIPTION', 'SYSTEM', 'CODE']
    medications_important_keys = ['START', 'STOP', 'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION', 'DISPENSES']
    encounters_important_keys = ['START', 'STOP', 'CODE', 'DESCRIPTION', 'REASONCODE', 'REASONDESCRIPTION']
    # get patient specific information from datasets
    if params == 'allergy':
        allergy_results = patient_record_collector(patient_id, allergy_collection)
        patient_electronic_health_record['allergy_formatted'] = format_dataset_record(allergy_results, allergy_important_keys) # formats the RAG data into a more easily processbale string for LLM summarisation model
        patient_electronic_health_record['allergy_raw'] = allergy_results # Raw RAG data objects for easy manipulation when building JSON response of specific patient data
        return patient_electronic_health_record
    if params == 'conditions':
        conditions_results = patient_record_collector(patient_id, condition_collection)
        patient_electronic_health_record['conditions_formatted'] = format_dataset_record(conditions_results, conditions_important_keys) # formats the RAG data into a more easily processbale string for LLM summarisation model
        patient_electronic_health_record['conditions_raw'] = conditions_results # Raw RAG data objects for easy manipulation when building JSON response of specific patient data
        return patient_electronic_health_record
    if params == 'medications': 
        medications_results = patient_record_collector(patient_id, medication_collection)
        patient_electronic_health_record['medications_formatted'] = format_dataset_record(medications_results, medications_important_keys) # formats the RAG data into a more easily processbale string for LLM summarisation model
        patient_electronic_health_record['medications_raw'] = medications_results # Raw RAG data objects for easy manipulation when building JSON response of specific patient data
        return patient_electronic_health_record
    if params == 'encounters':
        encounters_results = patient_record_collector(patient_id, encounter_collection)
        patient_electronic_health_record['appointments_formatted'] = format_dataset_record(encounters_results, encounters_important_keys) # formats the RAG data into a more easily processbale string for LLM summarisation model
        patient_electronic_health_record['appointments_raw'] = encounters_results # Raw RAG data objects for easy manipulation when building JSON response of specific patient data
        return patient_electronic_health_record
    

# Formats the retrived patient data by converting Python dictionary into a string and seperating entries with the | for simplified individual item extraction    
def format_dataset_record(retrieval_results, keys):
    formatted_records = []
    for record in retrieval_results:
        parts = [f"{key}: {record[key]}" for key in keys if key in record and record[key] not in (None, 'null')]
        formatted_records.append(", ".join(parts))
    return " | ".join(formatted_records)


# Queries the vector db for specific patient data
def patient_record_collector(patient_id, collection_obj):
     results = collection_obj.get(where={"PATIENT": patient_id})
     metadatas = results.get('metadatas', [])
     return metadatas

# Fetches the active medication for a specific patient
def get_patient_active_medication(patient_id):
    results = medication_collection.get(where={"PATIENT": patient_id})
    metadatas = results.get('metadatas', [])
    filtered_metadatas = [md for md in metadatas if "STOP" not in md]
    return filtered_metadatas

# Extracts the name of drugs from the retrieved medication data preapring it for drug drug interaction model
def extract_drug_names(list_of_drugs):
    list_of_cleaned_names = []
    for i in list_of_drugs:
        for a in (i['DESCRIPTION'].split('/')):
            cleaned_name = ''.join([char for char in a if not char.isdigit()]).replace('MG', '').replace('ML','').replace('Oral', '').replace('Tablet', '').strip()
            list_of_cleaned_names.append(cleaned_name)
            print(cleaned_name)
    return list_of_cleaned_names

def similar_record_context_search(query_text, collection_obj, top_k=1):
    print("query_text", query_text)
    query_embedding = model.encode([query_text]).tolist()
    results = collection_obj.query(
        query_embeddings = query_embedding,
        n_results = top_k,
        include = ["documents", "metadatas", "distances"]
    )
    return results

# Comment out the Medimate_backend inmports and uncomment code below. Run file to create vector database embeddings. Once created return code to previous state.

# chroma_client = chromadb.PersistentClient(path='A:\Dissertation\MediMate\chroma_db')
# allergy_collection = chroma_client.get_or_create_collection(name='allergy_collection')
# condition_collection = chroma_client.get_or_create_collection(name='condition_collections')
# encounter_collection = chroma_client.get_or_create_collection(name='encounter_collection')
# medication_collection = chroma_client.get_or_create_collection(name='medication_collection')
# drug_interaction_collection = chroma_client.get_or_create_collection(name='drug_drug_interaction_collection')
# model = SentenceTransformer('all-MiniLM-L6-v2')
# load_dataset()