import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def validate_input(text):
    if text.strip() == "":
        return False
    return True


def summarize_notes(user_notes):
    system_prompt = (
        "You are a helpful study assistant for students. You summarize notes "
        "clearly and concisely, using simple language a student can quickly revise from."
    )

    user_prompt = f"""Summarize the following notes into 5-7 clear bullet points.
Keep it concise and easy to revise from. Do not add information that isn't in the notes.

Notes:
{user_notes}"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"DEBUG ERROR: {e}"


def generate_quiz(user_notes):
    system_prompt = (
        "You are a helpful study assistant for students. You create short, clear "
        "quiz questions from notes to help students test their understanding."
    )

    user_prompt = f"""Create a short quiz of exactly 5 multiple-choice questions based on the following notes.
Each question should have 4 options labeled A-D, with only one correct answer.
Format each question and its options on separate lines, like this:

1. Question text?
A. Option one
B. Option two
C. Option three
D. Option four

After all questions, provide an answer key on separate lines, one per question.
Do not include information that isn't in the notes.

Notes:
{user_notes}"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"DEBUG ERROR: {e}"


if __name__ == "__main__":
    sample_notes = "Photosynthesis is the process by which plants convert sunlight into energy. It occurs in chloroplasts and produces oxygen as a byproduct."

    if validate_input(sample_notes):
        print(summarize_notes(sample_notes))
        print(generate_quiz(sample_notes))
    else:
        print("Invalid input, please enter some notes.")