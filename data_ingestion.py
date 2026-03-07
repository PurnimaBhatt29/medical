"""
Medical Dataset Ingestion Script
Downloads, preprocesses, and indexes medical datasets into Chroma vector database.
Must be run before launching the Streamlit application.
"""

import requests
import json
from typing import List, Dict
from utils.text_processing import clean_medical_text, parent_child_chunking
from utils.rag_pipeline import RAGPipeline
from sentence_transformers import SentenceTransformer, CrossEncoder
import config
import os
from tqdm import tqdm


class MedicalDataIngestion:
    """
    Handles ingestion of medical datasets into vector database.
    """
    
    def __init__(self):
        print("Initializing Medical Data Ingestion System...")
        
        # Initialize embedding model
        print(f"Loading embedding model: {config.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        
        # Initialize cross-encoder
        print(f"Loading cross-encoder: {config.CROSS_ENCODER_MODEL}")
        self.cross_encoder = CrossEncoder(config.CROSS_ENCODER_MODEL)
        
        # Initialize RAG pipeline (with dummy LLM for ingestion)
        # Initialize LLM with Groq
        if not config.GROQ_API_KEY:
            print("⚠️ GROQ_API_KEY is required for data ingestion. Please set it in your .env file.")
            return
        
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            api_key=config.GROQ_API_KEY,
            model_name=config.GROQ_MODEL,
            temperature=0.3
        )

        self.rag_pipeline = RAGPipeline(
            llm=llm,
            embedding_model_name=config.EMBEDDING_MODEL,
            cross_encoder_name=config.CROSS_ENCODER_MODEL,
            chroma_persist_dir=config.CHROMA_PERSIST_DIR
        )
        
        print("Initialization complete!\n")
    
    def ingest_fda_drug_labels(self, limit: int = 100):
        """
        Ingest FDA drug label data.
        """
        print("=" * 60)
        print("INGESTING FDA DRUG LABELS")
        print("=" * 60)
        
        try:
            # Fetch FDA drug labels
            print(f"Fetching FDA drug labels (limit: {limit})...")
            url = f"https://api.fda.gov/drug/label.json?limit={limit}"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"⚠️ FDA API returned status {response.status_code}")
                self._ingest_sample_drug_data()
                return
            
            data = response.json()
            results = data.get('results', [])
            
            print(f"Retrieved {len(results)} drug labels")
            
            # Process each drug label
            documents = []
            metadatas = []
            ids = []
            
            for idx, drug in enumerate(tqdm(results, desc="Processing drug labels")):
                drug_name = drug.get('openfda', {}).get('brand_name', ['Unknown'])[0]
                
                # Extract relevant sections
                sections = {
                    'indications': drug.get('indications_and_usage', [''])[0],
                    'dosage': drug.get('dosage_and_administration', [''])[0],
                    'contraindications': drug.get('contraindications', [''])[0],
                    'warnings': drug.get('warnings_and_cautions', [''])[0],
                    'adverse_reactions': drug.get('adverse_reactions', [''])[0],
                }
                
                # Create document for each section
                for section_name, section_text in sections.items():
                    if section_text and len(section_text) > 50:
                        cleaned_text = clean_medical_text(section_text)
                        
                        documents.append(cleaned_text)
                        metadatas.append({
                            'drug_name': drug_name,
                            'section': section_name,
                            'source': 'FDA',
                            'type': 'drug_label'
                        })
                        ids.append(f"fda_drug_{idx}_{section_name}")
            
            # Add to vector database
            print(f"\nAdding {len(documents)} documents to vector database...")
            self.rag_pipeline.add_documents(
                collection_name="medical_knowledge",
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✓ Successfully ingested {len(documents)} FDA drug label sections\n")
            
        except Exception as e:
            print(f"⚠️ Error ingesting FDA data: {e}")
            print("Falling back to sample data...")
            self._ingest_sample_drug_data()
    
    def _ingest_sample_drug_data(self):
        """Ingest sample drug data as fallback"""
        print("Ingesting sample drug data...")
        
        sample_drugs = [
            {
                'name': 'Metformin',
                'indications': 'Metformin is indicated as an adjunct to diet and exercise to improve glycemic control in adults and pediatric patients 10 years of age and older with type 2 diabetes mellitus.',
                'contraindications': 'Metformin is contraindicated in patients with severe renal impairment (eGFR below 30 mL/min/1.73 m²), acute or chronic metabolic acidosis, and hypersensitivity to metformin.',
                'dosage': 'The usual starting dose is 500 mg twice daily or 850 mg once daily with meals. Dosage may be increased gradually up to 2000 mg per day.',
                'warnings': 'Lactic acidosis is a rare but serious complication. Risk factors include renal impairment, hepatic impairment, and excessive alcohol intake.'
            },
            {
                'name': 'Amoxicillin',
                'indications': 'Amoxicillin is indicated for the treatment of infections due to susceptible strains of bacteria including respiratory tract infections, urinary tract infections, and skin infections.',
                'contraindications': 'Contraindicated in patients with a history of allergic reactions to any penicillin or cephalosporin antibiotics.',
                'dosage': 'Adults: 250-500 mg every 8 hours or 500-875 mg every 12 hours. Children: dosage based on body weight.',
                'warnings': 'Serious and occasionally fatal hypersensitivity reactions have been reported. Clostridium difficile-associated diarrhea may occur.'
            },
            {
                'name': 'Lisinopril',
                'indications': 'Lisinopril is indicated for the treatment of hypertension, heart failure, and to improve survival after myocardial infarction.',
                'contraindications': 'Contraindicated in patients with a history of angioedema related to ACE inhibitor therapy and in patients with hereditary or idiopathic angioedema.',
                'dosage': 'Hypertension: Initial dose 10 mg once daily. Usual maintenance dose 20-40 mg once daily.',
                'warnings': 'May cause fetal toxicity when administered to pregnant women. Discontinue as soon as pregnancy is detected.'
            },
            {
                'name': 'Atorvastatin',
                'indications': 'Atorvastatin is indicated to reduce the risk of cardiovascular events and to treat high cholesterol and triglyceride levels.',
                'contraindications': 'Contraindicated in patients with active liver disease, during pregnancy, and while breastfeeding.',
                'dosage': 'Initial dose: 10-20 mg once daily. Range: 10-80 mg once daily.',
                'warnings': 'Myopathy and rhabdomyolysis have been reported. Monitor liver enzymes before and during treatment.'
            },
            {
                'name': 'Omeprazole',
                'indications': 'Omeprazole is indicated for the treatment of gastroesophageal reflux disease (GERD), peptic ulcer disease, and Zollinger-Ellison syndrome.',
                'contraindications': 'Contraindicated in patients with known hypersensitivity to omeprazole or any component of the formulation.',
                'dosage': 'GERD: 20 mg once daily for 4-8 weeks. Peptic ulcer: 20-40 mg once daily.',
                'warnings': 'Long-term use may increase risk of bone fractures, vitamin B12 deficiency, and Clostridium difficile infection.'
            }
        ]
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, drug in enumerate(sample_drugs):
            for section in ['indications', 'contraindications', 'dosage', 'warnings']:
                text = drug.get(section, '')
                if text:
                    documents.append(clean_medical_text(text))
                    metadatas.append({
                        'drug_name': drug['name'],
                        'section': section,
                        'source': 'Sample',
                        'type': 'drug_label'
                    })
                    ids.append(f"sample_drug_{idx}_{section}")
        
        self.rag_pipeline.add_documents(
            collection_name="medical_knowledge",
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Successfully ingested {len(documents)} sample drug documents\n")
    
    def ingest_medical_conditions(self):
        """Ingest medical conditions and treatments"""
        print("=" * 60)
        print("INGESTING MEDICAL CONDITIONS DATA")
        print("=" * 60)
        
        # Sample medical conditions data
        conditions = [
            {
                'name': 'Type 2 Diabetes',
                'description': 'Type 2 diabetes is a chronic condition that affects the way the body processes blood sugar (glucose). The body either resists the effects of insulin or doesn\'t produce enough insulin to maintain normal glucose levels.',
                'symptoms': 'Increased thirst, frequent urination, increased hunger, unintended weight loss, fatigue, blurred vision, slow-healing sores, frequent infections.',
                'treatment': 'Treatment includes lifestyle changes (diet and exercise), oral medications like metformin, and insulin therapy if needed. Regular blood sugar monitoring is essential.',
                'risk_factors': 'Obesity, sedentary lifestyle, family history, age over 45, high blood pressure, abnormal cholesterol levels.'
            },
            {
                'name': 'Hypertension',
                'description': 'Hypertension (high blood pressure) is a condition in which the force of blood against artery walls is consistently too high, potentially leading to heart disease, stroke, and other complications.',
                'symptoms': 'Often asymptomatic. Severe hypertension may cause headaches, shortness of breath, nosebleeds, or chest pain.',
                'treatment': 'Lifestyle modifications (reduced sodium, exercise, weight loss) and medications including ACE inhibitors, ARBs, diuretics, beta-blockers, and calcium channel blockers.',
                'risk_factors': 'Age, family history, obesity, physical inactivity, tobacco use, high sodium diet, excessive alcohol consumption, stress.'
            },
            {
                'name': 'Pneumonia',
                'description': 'Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus, causing cough with phlegm, fever, chills, and difficulty breathing.',
                'symptoms': 'Cough with phlegm, fever, chills, shortness of breath, chest pain when breathing or coughing, fatigue, nausea, vomiting.',
                'treatment': 'Antibiotics for bacterial pneumonia, antivirals for viral pneumonia, antifungals for fungal pneumonia. Supportive care includes rest, fluids, and fever reducers.',
                'risk_factors': 'Age (very young or elderly), weakened immune system, chronic diseases, smoking, hospitalization, mechanical ventilation.'
            },
            {
                'name': 'Gastroesophageal Reflux Disease (GERD)',
                'description': 'GERD is a chronic digestive disorder where stomach acid or bile flows back into the esophagus, irritating the lining and causing symptoms.',
                'symptoms': 'Heartburn, regurgitation of food or sour liquid, difficulty swallowing, chest pain, chronic cough, laryngitis, disrupted sleep.',
                'treatment': 'Lifestyle changes (weight loss, avoiding trigger foods), antacids, H2 blockers, proton pump inhibitors (PPIs) like omeprazole, and in severe cases, surgery.',
                'risk_factors': 'Obesity, pregnancy, smoking, hiatal hernia, delayed stomach emptying, connective tissue disorders.'
            },
            {
                'name': 'Bacterial Infections',
                'description': 'Bacterial infections are caused by harmful bacteria entering the body and multiplying, potentially affecting various organs and systems.',
                'symptoms': 'Vary by infection site but may include fever, inflammation, pain, redness, swelling, discharge, and systemic symptoms.',
                'treatment': 'Antibiotics specific to the bacterial strain. Common antibiotics include amoxicillin, azithromycin, ciprofloxacin, and doxycycline.',
                'risk_factors': 'Weakened immune system, poor hygiene, close contact with infected individuals, chronic diseases, invasive medical procedures.'
            }
        ]
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, condition in enumerate(conditions):
            # Create comprehensive document
            full_text = f"""
Disease: {condition['name']}

Description: {condition['description']}

Symptoms: {condition['symptoms']}

Treatment: {condition['treatment']}

Risk Factors: {condition['risk_factors']}
"""
            cleaned_text = clean_medical_text(full_text)
            
            documents.append(cleaned_text)
            metadatas.append({
                'disease_name': condition['name'],
                'source': 'Medical Knowledge Base',
                'type': 'disease_info'
            })
            ids.append(f"condition_{idx}")
        
        self.rag_pipeline.add_documents(
            collection_name="medical_knowledge",
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Successfully ingested {len(documents)} medical condition documents\n")
    
    def run_full_ingestion(self):
        """Run complete data ingestion pipeline"""
        print("\n" + "=" * 60)
        print("STARTING MEDICAL KNOWLEDGE BASE INGESTION")
        print("=" * 60 + "\n")
        
        # Create persist directory if it doesn't exist
        os.makedirs(config.CHROMA_PERSIST_DIR, exist_ok=True)
        
        # Ingest all datasets
        self.ingest_fda_drug_labels(limit=50)
        self.ingest_medical_conditions()
        
        print("=" * 60)
        print("INGESTION COMPLETE!")
        print("=" * 60)
        print("\nMedical knowledge base is ready.")
        print(f"Vector database location: {config.CHROMA_PERSIST_DIR}")
        print("\nYou can now run the Streamlit application:")
        print("  streamlit run app.py\n")


if __name__ == "__main__":
    ingestion = MedicalDataIngestion()
    ingestion.run_full_ingestion()
