from sentence_transformers import SentenceTransformer
from clean_description import clean_description

model = SentenceTransformer('all-mpnet-base-v2')

def get_embedding(text):
    cleaned_text = clean_description(text)
    embedding = model.encode([cleaned_text])
    return embedding