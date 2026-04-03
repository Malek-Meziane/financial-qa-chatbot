from sentence_transformers import SentenceTransformer

def embed_chunks(chunks: list) -> list:
    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["chunk"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Created {len(embeddings)} embeddings")
    return embeddings.tolist(), chunks