# Document Q&A Assistant (RAG)

A Streamlit app that lets users upload a PDF or text document and ask questions about it. Answers are grounded in the document's actual content using a Retrieval-Augmented Generation (RAG) pipeline — not generated from the model's general knowledge.

## Features
- Upload a PDF or TXT document
- Ask natural-language questions about the document
- Answers are generated using only retrieved, relevant sections of the document
- Retrieved source chunks are shown alongside the answer for transparency
- Handles invalid/empty files and empty questions gracefully

## How it works (RAG pipeline)
1. **Text extraction** — the uploaded PDF/TXT is parsed into plain text (`pypdf` for PDFs, direct decode for TXT).
2. **Chunking** — the extracted text is split into overlapping chunks (500 characters, 100-character overlap) so ideas near chunk boundaries aren't lost.
3. **Embedding generation** — each chunk is converted into a 384-dimension vector using a local `sentence-transformers` model (`all-MiniLM-L6-v2`), capturing its meaning numerically.
4. **Retrieval** — when a question is asked, it's embedded the same way, then compared against every chunk's embedding using cosine similarity. The top 4 most similar chunks are selected.
5. **Grounded answer generation** — only the retrieved chunks (not the whole document) are sent to the LLM (via Groq) along with the question, with explicit instructions to answer only from that context, and to say "I cannot find this information in the document" if the answer isn't present — reducing hallucination.
6. **Source display** — the retrieved chunks are shown in expandable sections, so the user can verify the answer against the actual source text.

## Design choices
- **Chunk size (500) with overlap (100):** balances giving the embedding model enough context per chunk while minimizing the chance of splitting a relevant idea across two chunks.
- **Cosine similarity:** compares the *direction* (meaning) of embeddings rather than raw distance, so chunk length doesn't skew relevance scoring.
- **Local embeddings, hosted LLM:** embeddings run locally (fast, free, no API needed) while the final answer generation uses a hosted LLM (Groq) for stronger reasoning.

## Setup
1. Install dependencies:

pip install -r requirements.txt

2. Create a `.env` file in this folder with your Groq API key:

GROQ_API_KEY=your_key_here

3. Run the app:

python -m streamlit run app.py
