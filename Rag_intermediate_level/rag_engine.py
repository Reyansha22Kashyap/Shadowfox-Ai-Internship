from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text(uploaded_file):
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text
            return full_text

        elif uploaded_file.name.endswith(".txt"):
            full_text = uploaded_file.read().decode("utf-8")
            return full_text

        else:
            return None

    except Exception as e:
        print(f"Error occurred during text extraction: {e}")
        return None

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    embeddings = embedding_model.encode(chunks)
    return embeddings


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    return dot_product / (magnitude1 * magnitude2)


def retrieve_relevant_chunks(question, chunks, chunk_embeddings, top_n=4):
    question_embedding = embedding_model.encode(question)

    similarities = []
    for i, chunk_embedding in enumerate(chunk_embeddings):
        score = cosine_similarity(question_embedding,  chunk_embedding)
        similarities.append((score, chunks[i]))

    similarities.sort(reverse=True)
    top_chunks = [chunk for score, chunk in similarities[:top_n]]

    return top_chunks

def generate_answer(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)

    prompt = f"""You are a helpful assistant that answers questions based only on the provided context.

Context:
{context}

Question: {question}

Answer the question using only the information in the context above.
If the answer cannot be found in the context, say "I cannot find this information in the document" instead of guessing.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, something went wrong while generating the answer. Please try again."


if __name__ == "__main__":
    sample_chunks = [
        "The sky is blue.",
        "Water boils at 100 degrees Celsius.",
        "Photosynthesis occurs in chloroplasts.",
        "The sun is a star located at the center of our solar system."
    ]
    embeddings = create_embeddings(sample_chunks)

    question = "What is the capital of India?"
    top_chunks = retrieve_relevant_chunks(question, sample_chunks, embeddings, top_n=2)

    print("Top relevant chunks:")
    for c in top_chunks:
        print("-", c)

    answer = generate_answer(question, top_chunks)
    print("\nAnswer:")
    print(answer)