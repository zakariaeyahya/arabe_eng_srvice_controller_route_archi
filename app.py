import streamlit as st
import requests
import json  # Assurez-vous d'importer le module json

# Titre de l'application
st.title("Traduction Darija <-> Anglais avec Similarité")

# Zone de texte pour l'entrée utilisateur en Darija
input_text = st.text_area("Entrez le texte en Darija :", "")

# Bouton pour déclencher la traduction et la recherche de similarités
if st.button("Traduire et Trouver des Similitudes"):
    if input_text:
        try:
            # Envoi de la requête POST à l'API FastAPI
            response = requests.post(
                "http://localhost:8000/predict/",
                json={"text": input_text},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()  # Gère les erreurs HTTP

            result = response.json()  # Récupère les résultats au format JSON

            # Affichage du texte original et traduit
            if "user_text" in result:
                st.write("Texte original (Darija) :", result["user_text"])
            if "translated_text" in result:
                st.write("Texte traduit (Anglais) :", result["translated_text"])

            # Affichage des résultats de similarité
            if "results" in result and isinstance(result["results"], list):
                st.subheader("Similitudes :")
                for idx, res in enumerate(result["results"], 1):
                    st.write(f"{idx}. Étiquette : {res.get('label_arb', 'N/A')}")
                    st.write(f"   Similarité : {res.get('similarity', 'N/A')}")
                    st.write(f"   Version anglaise : {res.get('label_eng', 'N/A')}")
                    st.write("---")

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion au serveur : {e}")
        except json.JSONDecodeError:
            st.error("Erreur lors de l'analyse de la réponse JSON")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {e}")
    else:
        st.warning("Veuillez entrer du texte en Darija.")
