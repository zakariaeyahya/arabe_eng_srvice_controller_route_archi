
# Projet Traduction et Similarité
## Description
Ce projet permet de traduire du texte entre le Français, l'Anglais et l'Arabe, tout en trouvant des similarités basées sur des embeddings sémantiques.

## Fonctionnalités
Traduction : Traduit le texte d'une langue source vers une langue cible sélectionnée.
Recherche de Similarités : Trouve les étiquettes les plus similaires à partir de l'embedding du texte traduit.
Composants Principaux
Application Web (Streamlit) : Interface utilisateur pour entrer du texte et visualiser les résultats de traduction et de similarité.
API (FastAPI) : Endpoint pour gérer les requêtes de traduction et de similarité.
Modèles NLP : Utilisation de Sentence Transformers pour l'encodage de texte et de modèles Seq2Seq pour la traduction.
## Technologies Utilisées
Python, FastAPI, Streamlit
Transformers (Hugging Face), Sentence Transformers
Pandas, scikit-learn
Comment Utiliser
Prérequis : Assurez-vous d'avoir Python installé.
## Installation des dépendances : Utilisez pip install -r requirements.txt pour installer toutes les bibliothèques requises.
## Lancer l'application :
Exécutez uvicorn app:app --reload pour démarrer l'API FastAPI.
Exécutez streamlit run app.py pour démarrer l'application Streamlit.
## Interface Utilisateur :
Sélectionnez la langue source et la langue cible.
Entrez du texte à traduire et recherchez des similitudes.
Endpoints API :
/predict/ : Endpoint POST pour la traduction et la recherche de similarités.
/download-data/ : Endpoint GET pour télécharger les données collectées au format JSON.
Contributions et Support
Pour contribuer ou signaler des problèmes, veuillez ouvrir une issue sur GitHub.

Auteurs:
yahya zakariae
