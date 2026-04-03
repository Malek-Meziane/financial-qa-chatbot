import streamlit as st
from src.pdf_loader import load_pdf
from src.chunker import chunk_pages
from src.embeddings import embed_chunks
from src.retriever import build_index, retrieve
from src.generator import generate_answer

st.set_page_config(
    page_title="Financial Report Q&A",
    page_icon="📄",
    layout="wide"
)

st.title("Financial Report Q&A")
st.caption("Upload any financial PDF and ask questions in plain English")

# ── File upload ───────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload a financial PDF",
    type="pdf"
)

if uploaded is None:
    st.info("Upload a PDF to get started")
    st.stop()

# ── Cached pipeline ───────────────────────────────────────
@st.cache_resource
def process_pdf(uploaded_file):
    with st.spinner("Reading PDF..."):
        pages = load_pdf(uploaded_file)

    with st.spinner("Splitting into chunks..."):
        chunks = chunk_pages(pages)

    with st.spinner("Building search index (this takes ~30 seconds)..."):
        embeddings, chunks = embed_chunks(chunks)
        index = build_index(embeddings, chunks)

    return index, chunks

index, chunks = process_pdf(uploaded)
st.success("Ready — ask me anything about your document")

st.divider()

# ── Question input ────────────────────────────────────────
question = st.text_input(
    "Ask a question about your document",
    placeholder="What was the total revenue in 2024?"
)

if not question:
    st.stop()

# ── Retrieve and generate ─────────────────────────────────
with st.spinner("Searching document..."):
    relevant_chunks = retrieve(question, index, chunks)

with st.spinner("Generating answer..."):
    answer = generate_answer(question, relevant_chunks)

# ── Display answer ────────────────────────────────────────
st.subheader("Answer")
st.write(answer)

st.divider()

# ── Show sources ──────────────────────────────────────────
st.subheader("Sources used")
for chunk in relevant_chunks:
    with st.expander(f"Page {chunk['page']}"):
        st.write(chunk['chunk'])