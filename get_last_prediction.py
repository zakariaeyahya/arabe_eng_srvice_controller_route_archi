def get_last_prediction(data_list):
    if data_list:
        return {"last_prediction": data_list[-1]}
    else:
        return {"message": "Aucune prédiction n'a été faite"}