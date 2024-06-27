import json
import pandas as pd

# Chemin vers votre fichier JSON d'entrée et fichier Excel de sortie
input_json_file = r"D:\bureau\stage\exe 2\second try\results.json"
output_excel_file = r"D:\bureau\stage\exe 2\second try\results.xlsx"

# Lecture du fichier JSON
with open(input_json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Liste pour stocker les données
rows = []

# Extraire les données nécessaires
for item in data:
    user_text = item['user_text']
    translated_text = item['translated_text']
    for result in item['results']:
        label = result['label']
        similarity = result['similarity']
        rows.append({
            'user_text': user_text,
            'translated_text': translated_text,
            'label': label,
            'similarity': similarity
        })

# Créer un DataFrame pandas
df = pd.DataFrame(rows)

# Enregistrer le DataFrame en fichier Excel
df.to_excel(output_excel_file, index=False, engine='openpyxl')

print(f"Les résultats ont été enregistrés dans : {output_excel_file}")
