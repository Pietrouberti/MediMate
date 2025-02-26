import pandas as pd 
import chromadb 
from sentence_transformers import SentenceTransformer

class VectorMedicalDataset:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path='./chroma_db')
        self.allergy_collection = self.chroma_client.get_or_create_collection(name='allergy_collection')
        self.condition_collection = self.chroma_client.get_or_create_collection(name='condition_collections')
        self.encounter_collection = self.chroma_client.get_or_create_collection(name='encounter_collection')
        self.medication_collection = self.chroma_client.get_or_create_collection(name='medication_collection')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def load_dataset(self):
        allergies_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/allergies.csv')
        conditions_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/conditions.csv')
        encounters_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/encounters.csv')
        medications_dataset = pd.read_csv('A:/Dissertation/MediMate/MediMate/Datasets/medications.csv')
        
        self.index_allergy_data(allergies_dataset)
        self.index_conditions_data(conditions_dataset)
        self.index_encounters_data(encounters_dataset)
        self.index_medications_data(medications_dataset)

    def generate_embeddings(self, df, embedding_columns):
        df['index_text'] = df[embedding_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        embeddings = self.model.encode(df['index_text'].tolist(), show_progress_bar=True)
        return df, embeddings

    def index_allergy_data(self, df):
        df, allergy_embeddings = self.generate_embeddings(df, ['DESCRIPTION', 'TYPE', 'CATEGORY', 'REACTION1', 'DESCRIPTION1', 'REACTION2', 'DESCRIPTION2'])
        for i, row in df.iterrows():
            self.allergy_collection.add(
                ids=[str(i)],
                embeddings=[allergy_embeddings[i].tolist()],
                documents=[row['index_text']],
                metadatas=[row.to_dict()]
            )
        
    def index_conditions_data(self, df):
        df, conditions_embeddings = self.generate_embeddings(df, ['DESCRIPTION'])
        for i, row in df.iterrows():
            self.condition_collection.add(
                ids=[str(i)],
                embeddings=[conditions_embeddings[i].tolist()],
                documents=[row['index_text']],
                metadatas=[row.to_dict()]
            )

    def index_encounters_data(self, df):
        df, encounters_embeddings = self.generate_embeddings(df, ['ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION'])
        for i, row in df.iterrows():
            self.encounter_collection.add(
                ids=[str(i)],
                embeddings=[encounters_embeddings[i].tolist()],
                documents=[row['index_text']],
                metadatas=[row.to_dict()]
            )

    def index_medications_data(self, df):
        df, medications_embeddings = self.generate_embeddings(df, ['DESCRIPTION', 'REASONDESCRIPTION'])
        for i, row in df.iterrows():
            self.medication_collection.add(
                ids=[str(i)],
                embeddings=[medications_embeddings[i].tolist()],
                documents=[row['index_text']],
                metadatas=[row.to_dict()]
            )
            
            
    # pending development of API endpoint 
    # def rag_entry_point(self, patient_id, query_text):
    #     self.allergy_collection = self.chroma_client.get_collection(name='allergy_collection')
    #     condition_collection = self.chroma_client.get_collection(name='condition_collections')
    #     encounter_collection = self.chroma_client.get_collection(name='encounter_collection')
    #     medication_collection = self.chroma_client.get_collection(name='medication_collection')
        
    def patient_record_collector(self, patient_id, collection_obj):
        results = collection_obj.get(where={"PATIENT": patient_id})
        return results

    def similar_record_context_search(self, query_text, collection_obj, top_k=2):
        query_embedding = self.model.encode([query_text]).tolist()
        results = collection_obj.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return results

# Example usage
vector_medical_dataset = VectorMedicalDataset()
print(vector_medical_dataset.patient_record_collector('4569671e-ed39-055f-8e78-422b96c9896b', vector_medical_dataset.allergy_collection))
