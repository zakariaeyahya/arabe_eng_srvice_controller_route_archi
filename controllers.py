from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import json
from services import translate_text, find_most_similar_labels, load_embeddings_and_labels

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les embeddings et les étiquettes à partir des fichiers
try:
    embeddings, labels = load_embeddings_and_labels()
except Exception as e:
    raise RuntimeError("Erreur lors du chargement des embeddings ou du fichier Excel : " + str(e))

# Initialiser l'application FastAPI
app = FastAPI()

# Modèle de requête
class TextRequest(BaseModel):
    text: str

# Liste pour stocker les données des requêtes
data_list = []

@app.post("/predict/")
def predict_route(request: TextRequest):
    try:
        user_text = request.text
        logger.info(f"Texte reçu : {user_text}")
        
        # Traduire le texte de l'utilisateur
        translated_text = translate_text(user_text, src_lang="arb", tgt_lang="eng")
        if not translated_text:
            raise ValueError("La traduction a échoué")
        
        logger.info(f"Texte traduit : {translated_text}")
        
        # Obtenir les étiquettes les plus similaires
        results = find_most_similar_labels(translated_text, embeddings, labels)
        
        # Ajouter les données à la liste
        data_list.append({
            "user_text": user_text,
            "translated_text": translated_text,
            "results": results
        })
        
        return {
            "user_text": user_text,
            "translated_text": translated_text,
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Erreur dans la fonction predict : {e}")
        raise HTTPException(status_code=500, detail=str(e))
     

@app.get("/download-data/")
def download_data():
    try:
        # Écrire les données dans un fichier JSON
        with open("data.json", "w") as json_file:
            json.dump(data_list, json_file, indent=4)
        
        return FileResponse("data.json", filename="data.json", media_type="application/json")
    
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise HTTPException(status_code=500, detail=str(e))
