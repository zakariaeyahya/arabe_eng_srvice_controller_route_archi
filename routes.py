from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from controllers import predict, download_data, clear_history, get_recent_predictions, get_stats,get_last_prediction
from models import TextRequest
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/predict/")
def predict_route(request: TextRequest):
    return predict(request)
@app.get("/last-prediction/")
def last_prediction_route():
    try:
        return get_last_prediction()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la dernière prédiction : {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/download-data/")
def download_data_route():
    try:
        data = download_data()
        if isinstance(data, FileResponse):
            return data
        elif isinstance(data, dict) or isinstance(data, list):
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            return JSONResponse(content=json.loads(json_str), headers={"Content-Type": "application/json; charset=utf-8"})
        else:
            return JSONResponse(content={"data": str(data)}, headers={"Content-Type": "application/json; charset=utf-8"})
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-history/")
def clear_history_route():
    try:
        return clear_history()
    except Exception as e:
        logger.error(f"Erreur lors de l'effacement de l'historique : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported-languages/")
def get_supported_languages():
    return {
        "supported_languages": [
            {"code": "fra", "name": "Français"},
            {"code": "eng", "name": "Anglais"},
            {"code": "arb", "name": "Arabe"}
        ]
    }

@app.get("/recent-predictions/")
def recent_predictions_route(limit: int = 5):
    try:
        return get_recent_predictions(limit)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prédictions récentes : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/")
def stats_route():
    try:
        return get_stats()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques : {e}")
        raise HTTPException(status_code=500, detail=str(e))
