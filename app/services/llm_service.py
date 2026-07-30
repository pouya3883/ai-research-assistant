import os

from dotenv import load_dotenv
from google import genai
from app.services.retrieval_service import retrieve_context
from app.models.answer import AnswerResponse, Citation
from app.services.prompt_service import build_prompt

load_dotenv()

gemini_client: genai.Client | None = None


def get_gemini_client() -> genai.Client:
    global gemini_client

    if gemini_client is None:
        gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    return gemini_client


def generate_answer(prompt: str) -> str:
    response = get_gemini_client().models.generate_content(
        model="gemini-3.1-flash-lite", contents=prompt
    )

    return response.text


def answer_question(document_id: str, question: str) -> AnswerResponse:
    retrieval = retrieve_context(document_id=document_id, question=question)

    prompt = build_prompt(question=question, retrieval=retrieval)

    answer = generate_answer(prompt=prompt)

    citations = [
        Citation(
            id=index,
            source=chunk.source,
            chunk_index=chunk.chunk_index,
            preview=chunk.content.strip().replace("\n", " ")[:200],
        )
        for index, chunk in enumerate(retrieval.results, start=1)
    ]

    return AnswerResponse(answer=answer, citations=citations)
