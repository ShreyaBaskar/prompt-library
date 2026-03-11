_model = None

def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: Could not load sentence-transformers model: {e}")
            _model = None
    return _model

def encode(texts):
    model = get_model()
    if model is None:
        return None
    return model.encode(texts)
