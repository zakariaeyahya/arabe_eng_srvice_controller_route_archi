import streamlit as st
import requests
import json

# Title of the application
st.title("Traduction et Similarité entre Français, Anglais et Arabe")

# Language options
language_options = {
    "fra": "Français",
    "eng": "Anglais",
    "arb": "Arabe"
}

# Source language dropdown
src_lang = st.selectbox("Langue source :", options=list(language_options.keys()), format_func=lambda x: language_options[x])

# Target language dropdown
tgt_lang = st.selectbox("Langue cible :", options=list(language_options.keys()), format_func=lambda x: language_options[x])

# Text area for user input
input_text = st.text_area("Entrez le texte :", "")

# Button to trigger translation and similarity search
if st.button("Traduire et Trouver des Similitudes"):
    if input_text:
        try:
            # Sending POST request to FastAPI with selected language options
            response = requests.post(
                "http://localhost:8000/predict/",
                json={"text": input_text,"src_lang": src_lang, "tgt_lang": tgt_lang},  # Adjusted to remove src_lang
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()  # Handling HTTP errors
            
            result = response.json()  # Retrieving results in JSON format
            
            # Displaying original and translated text
            if "user_text" in result:
                st.write(f"Texte original ({language_options[src_lang]}) :", result["user_text"])
            if "translated_text" in result:
                st.write(f"Texte traduit ({language_options[tgt_lang]}) :", result["translated_text"])
            
            # Displaying similarity results
            if "results" in result and isinstance(result["results"], list):
                st.subheader(f"Similitudes ({language_options[tgt_lang]}) :")
                for idx, res in enumerate(result["results"], 1):
                    st.write(f"{idx}. Étiquette : {res.get('label', 'N/A')}")
                    st.write(f"   Similarité : {res.get('similarity', 'N/A')}")
                    st.write("---")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion au serveur : {e}")
        except json.JSONDecodeError:
            st.error("Erreur lors de l'analyse de la réponse JSON")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {e}")
    else:
        st.warning("Veuillez entrer du texte.")
