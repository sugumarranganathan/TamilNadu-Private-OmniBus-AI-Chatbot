import os
import google.generativeai as genai

from prompts import build_prompt

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_answer(question, context):

    prompt = build_prompt(question, context)

    response = model.generate_content(prompt)

    return response.text
