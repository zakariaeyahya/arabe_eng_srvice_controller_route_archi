from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from services import translate_text, find_most_similar_labels, load_embeddings_and_labels
import json
# Ajoutez ceci à vos imports dans controllers.py
from fastapi.responses import FileResponse

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
    src_lang: str
    tgt_lang: str

# Liste pour stocker les données des requêtes
data_list = []

@app.post("/predict/")
def predict(request: TextRequest):
    try:
        user_text = request.text
        src_lang = request.src_lang
        tgt_lang = request.tgt_lang
        logger.info(f"Texte reçu : {user_text}, Langue source : {src_lang}, Langue cible : {tgt_lang}")

        # Traduire le texte de l'utilisateur
        translated_text = translate_text(user_text, src_lang=src_lang, tgt_lang=tgt_lang)
        if not translated_text:
            raise ValueError("La traduction a échoué")

        logger.info(f"Texte traduit : {translated_text}")

        # Obtenir les étiquettes les plus similaires
        results = find_most_similar_labels(translated_text, embeddings, labels, tgt_lang=tgt_lang)

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
