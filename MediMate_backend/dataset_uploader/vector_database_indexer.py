import pandas as pd 
import chromadb 
import os
from sentence_transformers import SentenceTransformer
# from MediMate_backend.settings import model, allergy_collection, encounter_collection, condition_collection, medication_collection, drug_interaction_collection

'''

Notes to self: 

Need to create helper function to effectivly wrangle the data to ensure no null values in indexable columns.
Load in 1000 patient dataset by executing file with load_dataset() as entry point


'''

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
        patient_electronic_health_record['allergy_formatted'] = format_dataset_record(allergy_results, allergy_important_keys)
        patient_electronic_health_record['allergy_raw'] = allergy_results
        return patient_electronic_health_record
    if params == 'conditions':
        conditions_results = patient_record_collector(patient_id, condition_collection)
        patient_electronic_health_record['conditions_formatted'] = format_dataset_record(conditions_results, conditions_important_keys)
        patient_electronic_health_record['conditions_raw'] = conditions_results
        return patient_electronic_health_record
    if params == 'medications': 
        medications_results = patient_record_collector(patient_id, medication_collection)
        patient_electronic_health_record['medications_formatted'] = format_dataset_record(medications_results, medications_important_keys)
        patient_electronic_health_record['medications_raw'] = medications_results
        return patient_electronic_health_record
    if params == 'encounters':
        encounters_results = patient_record_collector(patient_id, encounter_collection)
        patient_electronic_health_record['appointments_formatted'] = format_dataset_record(encounters_results, encounters_important_keys)
        patient_electronic_health_record['appointments_raw'] = encounters_results
        return patient_electronic_health_record
    

# formats the retrived patient data by converting Python dictionary into a string and seperating entries with the | for simplified individual item extraction    
def format_dataset_record(retrieval_results, keys):
    formatted_records = []
    for record in retrieval_results:
        parts = [f"{key}: {record[key]}" for key in keys if key in record and record[key] not in (None, 'null')]
        formatted_records.append(", ".join(parts))
    return " | ".join(formatted_records)


# queries the vector db for specific patient data
def patient_record_collector(patient_id, collection_obj):
     results = collection_obj.get(where={"PATIENT": patient_id})
     metadatas = results.get('metadatas', [])
     return metadatas


# will be used to search for top_k amount of similar data entries using the query text parameter
def similar_record_context_search(query_text, collection_obj, top_k=2):
    query_embedding = model.encode([query_text]).tolist()
    results = collection_obj.query(
        query_embeddings = query_embedding,
        n_results = top_k,
        include = ["documents", "metadatas", "distances"]
    )
    return results

def get_patient_active_medication(patient_id):
    results = medication_collection.get(where={"PATIENT": patient_id})
    metadatas = results.get('metadatas', [])
    filtered_metadatas = [md for md in metadatas if "STOP" not in md]
    return filtered_metadatas

def extract_drug_names(list_of_drugs):
    list_of_cleaned_names = []
    for i in list_of_drugs:
        for a in (i['DESCRIPTION'].split('/')):
            cleaned_name = ''.join([char for char in a if not char.isdigit()]).replace('MG', '').replace('ML','').replace('Oral', '').replace('Tablet', '').strip()
            list_of_cleaned_names.append(cleaned_name)
            print(cleaned_name)
    return list_of_cleaned_names


# Comment out the Medimate_backend inmports and uncomment code below. Run file to create vector database embeddings. Once created return code to previous state.

chroma_client = chromadb.PersistentClient(path='A:\Dissertation\MediMate\chroma_db')
allergy_collection = chroma_client.get_or_create_collection(name='allergy_collection')
condition_collection = chroma_client.get_or_create_collection(name='condition_collections')
encounter_collection = chroma_client.get_or_create_collection(name='encounter_collection')
medication_collection = chroma_client.get_or_create_collection(name='medication_collection')
drug_interaction_collection = chroma_client.get_or_create_collection(name='drug_drug_interaction_collection')
model = SentenceTransformer('all-MiniLM-L6-v2')
# load_dataset()
k = get_patient_active_medication('34a4dcc4-35fb-6ad5-ab98-be285c586a4f')
extract_drug_names(k)