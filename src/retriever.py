import faiss
import numpy as np
import pickle
import os
import google.generativeai as genai
from dotenv import load_dotenv

def build_index(embeddings, chunks):
    vectors = np.array(embeddings, dtype=np.float32)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(vectors)
    faiss.write_index(index, "index.faiss")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"Index built with {index.ntotal} vectors")
    return index


def load_index():
    index = faiss.read_index("index.faiss")

    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    print(f"Loaded index with {index.ntotal} vectors")
    return index, chunks


def retrieve(question: str, index, chunks: list, top_k: int = 3) -> list:
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    question_vector = np.array([model.encode(question)], dtype=np.float32)

    distances, indices = index.search(question_vector, top_k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])

    return results