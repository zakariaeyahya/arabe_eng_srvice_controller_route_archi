import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import re
import torch
from sklearn.metrics.pairwise import cosine_similarity
import logging
import json
from fastapi.responses import FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

combined_embeddings_file = r'D:\bureau\stage\exe 2\second try\combined_embeddings_all-mpnet-base-v2.csv'
excel_file_path = r'd:\bureau\stage\exe 2\second try\classeur1.ods'

model = SentenceTransformer('all-mpnet-base-v2')
translation_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/seamless-m4t-v2-large")
processor = AutoTokenizer.from_pretrained("facebook/seamless-m4t-v2-large")

data_list = []

def clean_description(description):
    cleaned_text = description.lower()
    cleaned_text = re.sub(r'[^A-Za-z0-9]+', ' ', cleaned_text)
    return cleaned_text

def get_embedding(text):
    cleaned_text = clean_description(text)
    embedding = model.encode([cleaned_text])
    return embedding

def translate_text(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text
    
    try:
        inputs = processor(text=text, src_lang=src_lang, return_tensors="pt")
        outputs = translation_model.generate(**inputs, tgt_lang=tgt_lang)
        
        if isinstance(outputs, tuple):
            outputs = outputs[0]
        
        if isinstance(outputs, torch.Tensor):
            outputs = outputs.tolist()
        
        if not isinstance(outputs, list) or not outputs:
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

def find_most_similar_labels(user_input, embeddings, labels, top_k=5):
    user_embedding = get_embedding(user_input)
    similarities = cosine_similarity(user_embedding, embeddings)[0]
    indices = similarities.argsort()[::-1][:top_k]
    
    results = []
    for idx in indices:
        label = labels[idx]
        results.append({
            "label": label,
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

def download_data():
    try:
        with open("data.json", "w") as json_file:
            json.dump(data_list, json_file, indent=4)
        return FileResponse("data.json", filename="data.json", media_type="application/json")
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise Exception(f"Erreur lors du téléchargement des données : {e}")

def clear_history():
    global data_list
    data_list.clear()
    return {"message": "Historique effacé avec succès"}

def get_last_prediction():
    if data_list:
        return {"last_prediction": data_list[-1]}
    else:
        return {"message": "Aucune prédiction n'a été faite"}

def get_stats():
    total_requests = len(data_list)
    languages_used = set()
    for item in data_list:
        languages_used.add(item.get('src_lang', ''))
        languages_used.add(item.get('tgt_lang', ''))
    languages_used.discard('')
    return {
        "total_requests": total_requests,
        "languages_used": list(languages_used)
    }

def get_supported_languages():
    return {
        "supported_languages": [
            {"code": "fra", "name": "Français"},
            {"code": "eng", "name": "Anglais"},
            {"code": "arb", "name": "Arabe"}
        ]
    }
