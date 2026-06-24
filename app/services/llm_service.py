import os

from dotenv import load_dotenv
from google import genai
from app.services.embedding_service import semantic_search_document

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
    results = semantic_search_document(document_id=document_id, query=question)

    contexts = [result["content"] for result in results]

    sources = [result["chunk_filename"] for result in results]

    answer = generate_answer(question=question, contexts=contexts)

    return {"answer": answer, "sources": sources}
