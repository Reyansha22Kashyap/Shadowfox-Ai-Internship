import streamlit as st
from summarizer import validate_input, summarize_notes, generate_quiz

st.title("Student Study Assistant")
st.write("Paste your notes below and choose what you'd like to generate.")

notes_input = st.text_area("Enter your notes here")

feature_choice = st.radio(
    "Choose a feature:",
    ("Summarize Notes", "Generate Quiz")
)

if st.button("Generate"):
    if validate_input(notes_input):
        with st.spinner("Generating your result..."):
            if feature_choice == "Summarize Notes":
                result = summarize_notes(notes_input)
            else:
                result = generate_quiz(notes_input)

        st.markdown(result)
    else:
        st.error("Please enter some notes before generating.")