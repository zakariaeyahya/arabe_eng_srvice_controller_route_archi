from fastapi import FastAPI, HTTPException
from controllers import predict, download_data
from models import TextRequest

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
 
app = FastAPI()

@app.post("/predict/")
def predict_route(request: TextRequest):
    return predict(request)

from fastapi.responses import JSONResponse
import json

@app.get("/download-data/")
def download_data_route():
    try:
        data = download_data()
        if isinstance(data, FileResponse):
            return data  # Si c'est un FileResponse, retournez-le directement
        elif isinstance(data, dict) or isinstance(data, list):
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            return JSONResponse(content=json.loads(json_str), headers={"Content-Type": "application/json; charset=utf-8"})
        else:
            # Si ce n'est ni un FileResponse ni un dict/list, convertissez-le en chaîne
            return JSONResponse(content={"data": str(data)}, headers={"Content-Type": "application/json; charset=utf-8"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))