import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_answer(question, context):

    prompt = f"""
You are a Tamil Nadu Private OmniBus AI Assistant.

Use ONLY the information below.

Context:

{context}

Question:

{question}

If the answer is not available in the context, politely say so.
"""

    response = model.generate_content(prompt)

    return response.text
