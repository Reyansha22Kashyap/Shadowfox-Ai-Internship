# AI-Powered Student Study Assistant

A simple Streamlit app that helps students study more effectively using an LLM (via Groq API).

## Features
- **Summarize Notes** — condenses pasted notes into 5-7 clear bullet points.
- **Generate Quiz** — creates a 5-question multiple-choice quiz (with answer key) from notes.

## How it works
1. User pastes notes into the text box.
2. User selects a feature (Summarize or Generate Quiz).
3. Input is validated (empty/whitespace input is rejected before calling the API).
4. The selected feature builds a structured prompt (system + user message) and sends it to the Groq API.
5. API errors are caught gracefully and shown as a friendly message.
6. The generated result is displayed on the page.

## Setup
1. Install dependencies:pip install -r requirements.txt
2. Create a `.env` file in the project root with your Groq API key:GROQ_API_KEY=your_key_here
3. Run the app:python -m streamlit run app.py
4. Save it (Ctrl+S)