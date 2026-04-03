import requests

def generate_answer(question: str, chunks: list) -> str:
    context = ""
    for chunk in chunks:
        context += f"Page {chunk['page']}:\n{chunk['chunk']}\n\n"

    prompt = f"""You are a financial analyst. You will be given context from a financial document and a question.

Rules:
- Answer using ONLY information from the context
- If the answer isn't in the context, say "I cannot find this in the provided documents"
- Always cite the page number at the end: (Source: page X)
- Be concise — 2-4 sentences for simple questions, longer only if needed

Context:
{context}

Question: {question}

Answer:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "temperature": 0.1,
            "stream": False
        }
    )

    return response.json()["response"]