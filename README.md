
# Projet de Traduction et Similarité
Ce projet vise à développer une application de traduction et de recherche de similarité entre textes, utilisant des modèles de transformation de phrases et des techniques de traitement du langage naturel (NLP). L'application est construite avec FastAPI pour le backend et Streamlit pour l'interface utilisateur.

## Fonctionnalités
Traduction : Traduit le texte d'une langue source à une langue cible à l'aide du modèle Seamless Translator.
Recherche de Similarité : Identifie les étiquettes les plus similaires au texte de l'utilisateur en utilisant des embeddings et la similarité cosinus.
Interface Utilisateur : Interface utilisateur simple avec Streamlit pour interagir avec les fonctionnalités backend.
## Architecture du Projet
Le projet est structuré comme suit :

app.py : Interface utilisateur avec Streamlit pour lancer les requêtes vers l'API FastAPI.
routes.py : Définition des routes FastAPI pour gérer les requêtes de traduction et de similarité.
controllers.py : Logique métier pour gérer les requêtes et appeler les fonctions de service.
services.py : Fonctions de service pour la traduction, la recherche de similarité et la gestion des données.
seamless_translator.py : Classe pour la traduction utilisant le modèle Seamless Translator.
data.json : Fichier de données pour enregistrer l'historique des requêtes.
results.json : Résultats formatés en JSON à partir des données d'entrée.
testenco.py : Script pour encoder et enregistrer les résultats au format JSON.
to_excel.py : Script pour convertir les résultats JSON en un fichier Excel structuré.
## Prérequis
Avant de démarrer, assurez-vous d'avoir les éléments suivants installés et configurés :

Python 3.x
Packages Python : fastapi, uvicorn, streamlit, pandas, sentence-transformers, transformers, torch, scikit-learn, etc.
Accès à un GPU pour des performances améliorées lors de l'utilisation de modèles NLP complexes.

## Utilisation
Lancez le serveur FastAPI :
Copy code
uvicorn app:app --reload
## Lancez l'interface utilisateur avec Streamlit :
streamlit run app.py
Accédez à l'application via votre navigateur à l'adresse : http://localhost:8501

## Contribution
Les contributions sont les bienvenues ! Pour des suggestions, des bugs ou des améliorations potentielles, veuillez ouvrir une issue ou soumettre une pull request.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.


