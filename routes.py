# Dans routes.py
from fastapi import FastAPI, HTTPException
from controllers import predict, download_data  # Importer directement les fonctions nécessaires
from models import TextRequest  # Importer la classe TextRequest depuis models.py

app = FastAPI()

@app.post("/predict/")
def predict_route(request: TextRequest):
    return predict(request)  # Utiliser la fonction predict définie dans controllers.py

@app.get("/download-data/")
def download_data_route():
    return download_data()  # Utiliser la fonction download_data définie dans controllers.py
