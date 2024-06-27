import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import re
import torch
from sklearn.metrics.pairwise import cosine_similarity
import logging
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File paths
combined_embeddings_file = r'D:\bureau\stage\exe 2\second try\combined_embeddings_all-mpnet-base-v2.csv'
excel_file_path = r'd:\bureau\stage\exe 2\second try\classeur1.ods'

# Load models
model = SentenceTransformer('all-mpnet-base-v2')
translation_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/seamless-m4t-v2-large")
processor = AutoTokenizer.from_pretrained("facebook/seamless-m4t-v2-large")

def clean_description(description):
    cleaned_text = description.lower()
    cleaned_text = re.sub(r'[^A-Za-z0-9]+', ' ', cleaned_text)
    return cleaned_text

def get_embedding(text):
    cleaned_text = clean_description(text)
    embedding = model.encode([cleaned_text])
    return embedding

def translate_text(text, src_lang, tgt_lang):
    try:
        inputs = processor(text=text, src_lang=src_lang, return_tensors="pt")
        outputs = translation_model.generate(**inputs, tgt_lang=tgt_lang)
        
        if isinstance(outputs, tuple):
            outputs = outputs[0]
        
        if isinstance(outputs, torch.Tensor):
            outputs = outputs.tolist()
        
        if not isinstance(outputs, list):
            return None
        
        if not outputs:
            return None
        
        if isinstance(outputs[0], list):
            decoded = processor.batch_decode(outputs, skip_special_tokens=True)
        else:
            decoded = processor.decode(outputs, skip_special_tokens=True)
        
        if isinstance(decoded, list):
            decoded = " ".join(decoded)
        
        logger.info(f"Translated text from {src_lang} to {tgt_lang}: {decoded}")
        
        return decoded
    
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return None

def find_most_similar_labels(user_input, embeddings, labels, tgt_lang, top_k=5):
    user_embedding = get_embedding(user_input)
    similarities = cosine_similarity(user_embedding, embeddings)[0]
    indices = similarities.argsort()[::-1][:top_k]
    
    results = []
    for idx in indices:
        label = labels[idx]
        translated_label = translate_text(label, src_lang="eng", tgt_lang=tgt_lang)
        results.append({
            "label": translated_label if translated_label else label,
            "similarity": float(similarities[idx])
        })
    
    return results

def load_embeddings_and_labels():
    try:
        logger.info(f"Attempting to load embeddings from {combined_embeddings_file}")
        df_embeddings = pd.read_csv(combined_embeddings_file)
        logger.info(f"Successfully loaded embeddings. Shape: {df_embeddings.shape}")

        logger.info(f"Attempting to load labels from {excel_file_path}")
        df_labels = pd.read_excel(excel_file_path, engine='odf')
        logger.info(f"Successfully loaded labels. Shape: {df_labels.shape}")

        embeddings = df_embeddings.values
        labels = df_labels['preferredLabel'].values
        return embeddings, labels
    except Exception as e:
        logger.error(f"Error loading embeddings or Excel file: {str(e)}")
        raise RuntimeError(f"Error loading embeddings or Excel file: {str(e)}")
# services/stats_service.py


def get_stats(data_list):
    try:
        total_requests = len(data_list)
        languages_used = set(item["src_lang"] for item in data_list) | set(item["tgt_lang"] for item in data_list)
        return {
            "total_requests": total_requests,
            "languages_used": list(languages_used)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
