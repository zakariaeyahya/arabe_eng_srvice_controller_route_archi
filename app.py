import streamlit as st
import requests
import json
from urllib.parse import quote

st.title("Traduction et Similarité entre Français, Anglais et Arabe")

language_options = {
    "fra": "Français",
    "eng": "Anglais",
    "arb": "Arabe"
}

src_lang = st.selectbox("Langue source :", options=list(language_options.keys()), format_func=lambda x: language_options[x])
tgt_lang = st.selectbox("Langue cible :", options=list(language_options.keys()), format_func=lambda x: language_options[x])

input_text = st.text_area("Entrez le texte :", "")

if st.button("Traduire et Trouver des Similitudes"):
    if input_text:
        try:
            # Encoder le texte pour l'URL
            encoded_text = quote(input_text)
            
            # Construire l'URL avec les paramètres
            url = f"http://localhost:8000/predict/?text={encoded_text}&src_lang={src_lang}&tgt_lang={tgt_lang}"
            
            response = requests.get(url)
            response.raise_for_status()
            
            result = response.json()
            
            if "user_text" in result:
                st.write(f"Texte original ({language_options[src_lang]}) :", result["user_text"])
            if "translated_text" in result:
                st.write(f"Texte traduit ({language_options[tgt_lang]}) :", result["translated_text"])
            
            if "results" in result and isinstance(result["results"], list):
                st.subheader(f"Similitudes ({language_options[src_lang]}) :")
                for idx, res in enumerate(result["results"], 1):
                    label = res.get("label", "N/A")
                    similarity = res.get("similarity", "N/A")
                    
                    st.write(f"{idx}. Étiquette : {label}")
                    st.write(f"   Similarité : {similarity:.4f}")
                    st.write("---")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion au serveur : {e}")
        except json.JSONDecodeError:
            st.error("Erreur lors de l'analyse de la réponse JSON")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {e}")
    else:
        st.warning("Veuillez entrer du texte.")

 
