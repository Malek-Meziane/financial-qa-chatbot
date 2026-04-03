# Financial Report Q&A Chatbot

A RAG (Retrieval Augmented Generation) pipeline that answers 
questions over any financial PDF with page citations.

## How it works
1. Upload any financial PDF (annual report, 10-K, earnings release)
2. App splits it into chunks and builds a searchable vector index
3. Ask questions in plain English
4. Get answers with exact page citations

## Results
- Retrieves relevant chunks using FAISS vector similarity search
- Generates grounded answers using Llama 3.2 (local, no API cost)
- Always cites the source page number

## Setup

### Requirements
- Python 3.10+
- [Ollama](https://ollama.com) with llama3.2 installed

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/financial-qa.git
cd financial-qa
python -m venv .venv
.venv\Scripts\activate.bat   # Windows
pip install -r requirements.txt
ollama pull llama3.2
```

### Run
```bash
streamlit run app.py
```

## Project structure
financial_qa/
├── src/
│   ├── pdf_loader.py        ← extracts text from PDF
│   ├── chunker.py           ← splits text into chunks
│   ├── embeddings.py        ← local embeddings with sentence-transformers
│   ├── retriever.py         ← FAISS vector search
│   └── generator.py         ← answer generation with Ollama
├── app.py                   ← Streamlit interface
└── requirements.txt

## Technical choices
- **sentence-transformers** — local embeddings, no API cost or rate limits
- **FAISS** — fast vector similarity search, scales to millions of chunks
- **Ollama + Llama 3.2** — local LLM, no API key needed, no cost
- **Chunk overlap** — 50 word overlap prevents answers being cut at boundaries

## What I'd add next
- Chat history so users can ask follow-up questions
- Support for multiple PDFs at once
- Better chunking using sentence boundaries instead of word count
- Confidence score per retrieved chunk