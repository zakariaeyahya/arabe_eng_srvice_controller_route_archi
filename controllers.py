from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from services import translate_text, find_most_similar_labels, load_embeddings_and_labels
import json
from fastapi.responses import FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    embeddings, labels = load_embeddings_and_labels()
except Exception as e:
    raise RuntimeError("Erreur lors du chargement des embeddings ou du fichier Excel : " + str(e))

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str

data_list = []

def predict(request: TextRequest):
    try:
        user_text = request.text
        src_lang = request.src_lang
        tgt_lang = request.tgt_lang
        logger.info(f"Texte reçu : {user_text}, Langue source : {src_lang}, Langue cible : {tgt_lang}")

        translated_text = translate_text(user_text, src_lang=src_lang, tgt_lang=tgt_lang)
        if not translated_text:
            raise ValueError("La traduction a échoué")

        logger.info(f"Texte traduit : {translated_text}")

        results = find_most_similar_labels(translated_text, embeddings, labels, tgt_lang=tgt_lang)
        logger.info(f"Résultats de similarité : {results}")

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

def download_data():
    try:
        with open("data.json", "w") as json_file:
            json.dump(data_list, json_file, indent=4)

        return FileResponse("data.json", filename="data.json", media_type="application/json")

    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def clear_history():
    global data_list
    data_list.clear()
    return {"message": "Historique effacé avec succès"}

def get_recent_predictions(limit: int = 5):
    return {"recent_predictions": data_list[-limit:]}
def get_last_prediction():
    if data_list:
        return {"last_prediction": data_list[-1]}
    else:
        return {"message": "Aucune prédiction n'a été faite"}
def get_stats():
    total_requests = len(data_list)
    languages_used = set(item["src_lang"] for item in data_list) | set(item["tgt_lang"] for item in data_list)
    return {
        "total_requests": total_requests,
        "languages_used": list(languages_used)
    }
