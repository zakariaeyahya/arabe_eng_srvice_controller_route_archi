from fastapi import FastAPI
from controllers import predict_route as predict, download_data
from models import TextRequest

app = FastAPI()

@app.post("/predict/")
def predict_route(request: TextRequest):
    return predict(request)

@app.get("/download-data/")
def download_data_route():
    return download_data()