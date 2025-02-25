import pandas as pd 
import chromadb 
from sentence_transformers import SentenceTransformer


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

def rag_entry_point(patient_id, query_text):
    allergy_collection = chroma_client.get_collection(name='allergy_collection')
    condition_collection = chroma_client.get_collection(name='condition_collections')
    encounter_collection = chroma_client.get_collection(name='encounter_collection')
    medication_collection = chroma_client.get_collection(name='medication_collection')
    
def patient_record_collector(patient_id, collection_obj):
     results = collection_obj.get(where={"PATIENT": patient_id})
     return results

def similar_record_context_search(query_text, collection_obj, top_k=2):
    query_embedding = model.encode([query_text]).tolist()
    results = collection_obj.query(
        query_embeddings = query_embedding,
        n_results = top_k,
        include = ["documents", "metadatas", "distances"]
    )
    return results
    

chroma_client = chromadb.PersistentClient(path='./chroma_db')
allergy_collection = chroma_client.get_or_create_collection(name='allergy_collection')
condition_collection = chroma_client.get_or_create_collection(name='condition_collections')
encounter_collection = chroma_client.get_or_create_collection(name='encounter_collection')
medication_collection = chroma_client.get_or_create_collection(name='medication_collection')
model = SentenceTransformer('all-MiniLM-L6-v2')

print(patient_record_collector('4569671e-ed39-055f-8e78-422b96c9896b', allergy_collection))
