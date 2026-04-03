def chunk_pages(pages: list) -> list:
    chunks = []
    chunk_size = 300
    overlap = 50
    step = chunk_size - overlap

    for page in pages:
        words = page["text"].split()

        for i in range(0, len(words), step):
            chunk_words = words[i : i + chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "page": page["page"],
                "chunk": chunk_text
            })

    print(f"Created {len(chunks)} chunks from {len(pages)} pages")
    return chunks