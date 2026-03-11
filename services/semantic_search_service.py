from utils.prompt_loader import load_prompts
from utils.embedding_loader import encode
import numpy as np

_prompt_embeddings = None
_prompts_for_embedding = None

def _build_embeddings():
    global _prompt_embeddings, _prompts_for_embedding
    prompts = load_prompts()
    texts = [f"{p['title']} {p['category']} {p['preview']} {' '.join(p.get('tags', []))}" for p in prompts]
    embeddings = encode(texts)
    if embeddings is not None:
        _prompt_embeddings = embeddings
        _prompts_for_embedding = prompts
        return True
    return False

def semantic_search(query, top_k=5):
    global _prompt_embeddings, _prompts_for_embedding
    
    if _prompt_embeddings is None:
        success = _build_embeddings()
        if not success:
            # Fallback to keyword search
            from services.search_service import keyword_search
            return keyword_search(query)
    
    query_embedding = encode([query])
    if query_embedding is None:
        from services.search_service import keyword_search
        return keyword_search(query)
    
    # Cosine similarity
    query_vec = query_embedding[0]
    scores = np.dot(_prompt_embeddings, query_vec) / (
        np.linalg.norm(_prompt_embeddings, axis=1) * np.linalg.norm(query_vec) + 1e-10
    )
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [_prompts_for_embedding[i] for i in top_indices]
