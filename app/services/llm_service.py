import os

from dotenv import load_dotenv
from google import genai
from app.services.embedding_service import build_context

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question: str, contexts: list[str]):
    context = "\n\n".join(contexts)

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer in English.

    Use only the provided context.
    If the context is written in another language, translate the relevant information to English before answering.
    """

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    return response.text


def answer_question(document_id: str, question: str):
    contexts = build_context(document_id=document_id, query=question)

    answer = generate_answer(question=question, contexts=contexts)

    return answer
