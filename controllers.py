from fastapi import HTTPException
import logging
from translate_text import translate_text
from find_most_similar_labels import find_most_similar_labels
from load_embeddings_and_labels import load_embeddings_and_labels
from download_data import download_data
from clear_history import clear_history
from get_last_prediction import get_last_prediction
from get_stats import get_stats
from get_supported_languages import get_supported_languages
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    embeddings, labels = load_embeddings_and_labels()
except Exception as e:
    raise RuntimeError("Erreur lors du chargement des embeddings ou du fichier Excel : " + str(e))

data_list = []

def predict_controller(text: str, src_lang: str, tgt_lang: str):
    try:
        logger.info(f"Texte reçu : {text}, Langue source : {src_lang}, Langue cible : {tgt_lang}")

        translated_text = translate_text(text, src_lang=src_lang, tgt_lang="eng")
        if not translated_text:
            raise ValueError("La traduction a échoué")

        logger.info(f"Texte traduit en anglais pour la recherche : {translated_text}")

        results = find_most_similar_labels(translated_text, embeddings, labels, top_k=5)
        
        results_in_source_language = []
        for res in results:
            source_label = res["label"]
            if src_lang != "eng":
                translated_label = translate_text(source_label, src_lang="eng", tgt_lang=src_lang)
                label_to_use = translated_label if translated_label else source_label
            else:
                label_to_use = source_label
            
            results_in_source_language.append({
                "label": label_to_use,
                "similarity": res["similarity"]
            })

        logger.info(f"Résultats de similarité : {results_in_source_language}")

        display_translated_text = translate_text(text, src_lang=src_lang, tgt_lang=tgt_lang) if src_lang != tgt_lang else text

        data_list.append({
            "user_text": text,
            "translated_text": display_translated_text,
            "results": results_in_source_language,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang
        })

        return {
            "user_text": text,
            "translated_text": display_translated_text,
            "results": results_in_source_language
        }

    except Exception as e:
        logger.error(f"Erreur dans la fonction predict : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def download_data_controller():
    try:
        return download_data(data_list)
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def clear_history_controller():
    try:
        return clear_history(data_list)
    except Exception as e:
        logger.error(f"Erreur lors de l'effacement de l'historique : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def last_prediction_controller():
    try:
        return get_last_prediction(data_list)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la dernière prédiction : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def stats_controller():
    try:
        return get_stats(data_list)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques : {e}")
        raise HTTPException(status_code=500, detail=str(e))
# Dans controllers.py, ajoutez cette fonction :

def supported_languages_controller():
    try:
        return get_supported_languages()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des langues supportées : {e}")
        raise HTTPException(status_code=500, detail=str(e))