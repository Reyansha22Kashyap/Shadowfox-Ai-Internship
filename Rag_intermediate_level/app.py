import streamlit as st
from rag_engine import extract_text, chunk_text, create_embeddings, retrieve_relevant_chunks, generate_answer

st.title("Document Q&A Assistant")
st.write("Upload a PDF and ask questions about its content.")

uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])

if uploaded_file is not None:
    st.write("File uploaded:", uploaded_file.name)

    document_text = extract_text(uploaded_file)

    if document_text is None or document_text.strip() == "":
        st.error("Could not extract any text from this file. It may be corrupted, empty, or an image-only (scanned) document.")
    else:
        chunks = chunk_text(document_text)
        chunk_embeddings = create_embeddings(chunks)

        st.write(f"Document processed into {len(chunks)} chunks.")

        question = st.text_input("Ask a question about the document")

        if st.button("Get Answer"):
            if question.strip() == "":
                st.error("Please enter a question.")
            else:
                with st.spinner("Searching document and generating answer..."):
                    top_chunks = retrieve_relevant_chunks(question, chunks, chunk_embeddings, top_n=4)
                    answer = generate_answer(question, top_chunks)

                st.subheader("Answer")
                st.write(answer)

                st.subheader("Retrieved Source Context")
                for i, chunk in enumerate(top_chunks):
                    with st.expander(f"Source chunk {i+1}"):
                        st.write(chunk)

    
    