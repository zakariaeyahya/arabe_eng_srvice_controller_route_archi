from fastapi import FastAPI
from controllers import predict_controller, download_data_controller, clear_history_controller, last_prediction_controller, stats_controller, supported_languages_controller
from models import TextRequest

app = FastAPI()

@app.post("/predict/")
def predict_route(request: TextRequest):
    return predict_controller(request)

@app.get("/download-data/")
def download_data_route():
    return download_data_controller()

@app.post("/clear-history/")
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
