from fastapi import HTTPException
from services import translate_text, find_most_similar_labels, load_embeddings_and_labels, download_data, clear_history, get_last_prediction, get_stats, get_supported_languages, data_list
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    embeddings, labels = load_embeddings_and_labels()
except Exception as e:
    raise RuntimeError("Erreur lors du chargement des embeddings ou du fichier Excel : " + str(e))

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
        return download_data()
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def clear_history_controller():
    try:
        return clear_history()
    except Exception as e:
        logger.error(f"Erreur lors de l'effacement de l'historique : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def last_prediction_controller():
    try:
        return get_last_prediction()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la dernière prédiction : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def stats_controller():
    try:
        return get_stats()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques : {e}")
        raise HTTPException(status_code=500, detail=str(e))

def supported_languages_controller():
    return get_supported_languages()
