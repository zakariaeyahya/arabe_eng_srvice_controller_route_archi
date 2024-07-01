from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeamlessTranslator:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Utilisation de l'appareil : {self.device}")
        
        self.translation_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/seamless-m4t-v2-large").to(self.device)
        self.processor = AutoTokenizer.from_pretrained("facebook/seamless-m4t-v2-large")

    def translate_text(self, text, src_lang, tgt_lang):
        try:
            if src_lang == tgt_lang:
                return text

            inputs = self.processor(text=text, src_lang=src_lang, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.translation_model.generate(
                    **inputs,
                    tgt_lang=tgt_lang,
                    max_length=100,
                    num_beams=5,
                    no_repeat_ngram_size=2
                )
            
            decoded = self.processor.batch_decode(outputs, skip_special_tokens=True)
            
            if isinstance(decoded, list):
                decoded = " ".join(decoded)
            
            logger.info(f"Texte traduit de {src_lang} à {tgt_lang}: {decoded}")
            
            return decoded
            
        except Exception as e:
            logger.error(f"Erreur de traduction: {e}")
            return None