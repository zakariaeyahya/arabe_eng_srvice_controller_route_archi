import json
import os

# Chemin vers votre fichier JSON d'entrée et de sortie
input_json_file = r"D:\bureau\stage\exe 2\second try\data.json"
output_json_file = r"D:\bureau\stage\exe 2\second try\results.json"

# Créer les répertoires nécessaires pour le fichier de sortie
output_dir = os.path.dirname(output_json_file)
os.makedirs(output_dir, exist_ok=True)

# Lecture du fichier en spécifiant l'encodage
with open(input_json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Structure pour stocker les résultats finaux
results_to_save = []

# Traiter chaque élément dans le fichier JSON d'entrée
for item in data:
    user_text = item['user_text']
    translated_text = item['translated_text']
    results = item['results']
    
    # Structure pour stocker les résultats de cet élément
    item_results = {
        'user_text': user_text,
        'translated_text': translated_text,
        'results': results
    }
    
    results_to_save.append(item_results)

# Enregistrer les résultats dans un nouveau fichier JSON
with open(output_json_file, 'w', encoding='utf-8') as f:
    json.dump(results_to_save, f, ensure_ascii=False, indent=4)

print(f"Les résultats ont été enregistrés dans : {output_json_file}")
