from fastapi import FastAPI, Query
from controllers import predict_controller, download_data_controller, clear_history_controller, last_prediction_controller, stats_controller, supported_languages_controller

app = FastAPI()

@app.get("/predict/")
def predict_route(
    text: str = Query(..., description="Texte à traduire et à analyser"),
    src_lang: str = Query(..., description="Code de la langue source"),
    tgt_lang: str = Query(..., description="Code de la langue cible")
):
    return predict_controller(text, src_lang, tgt_lang)

@app.get("/download-data/")
def download_data_route():
    return download_data_controller()

@app.get("/clear-history/")
def clear_history_route():
    return clear_history_controller()

@app.get("/last-prediction/")
def last_prediction_route():
    return last_prediction_controller()

@app.get("/stats/")
def stats_route():
    return stats_controller()

@app.get("/supported-languages/")
def supported_languages_route():
    return supported_languages_controller()
