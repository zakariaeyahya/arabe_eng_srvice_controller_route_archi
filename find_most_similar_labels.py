from sklearn.metrics.pairwise import cosine_similarity
from get_embedding import get_embedding

def find_most_similar_labels(user_input, embeddings, labels, top_k=5):
    user_embedding = get_embedding(user_input)
    similarities = cosine_similarity(user_embedding, embeddings)[0]
    indices = similarities.argsort()[::-1][:top_k]
    
    results = []
    for idx in indices:
        label = labels[idx]
        results.append({
            "label": label,
            "similarity": float(similarities[idx])
        })
    
    return results