import os

from dotenv import load_dotenv
from google import genai
from app.services.embedding_service import semantic_search_document
from app.models.answer import AnswerResponse
from app.services.prompt_service import build_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(prompt: str):
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    return response.text


def answer_question(document_id: str, question: str):
    results = semantic_search_document(document_id=document_id, query=question)

    contexts = [result["content"] for result in results]

    sources = [result["chunk_filename"] for result in results]

    prompt = build_prompt(question=question, contexts=contexts)

    answer = generate_answer(prompt=prompt)

    return AnswerResponse(answer=answer, sources=sources)
