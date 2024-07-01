import json
from fastapi.responses import FileResponse
import logging

logger = logging.getLogger(__name__)

def download_data(data_list):
    try:
        with open("data.json", "w") as json_file:
            json.dump(data_list, json_file, indent=4)
        return FileResponse("data.json", filename="data.json", media_type="application/json")
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement des données : {e}")
        raise Exception(f"Erreur lors du téléchargement des données : {e}")