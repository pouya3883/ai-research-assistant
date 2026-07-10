import os

from dotenv import load_dotenv
from google import genai
from app.services.retrieval_service import retrieve_context
from app.models.answer import AnswerResponse, Citation
from app.services.prompt_service import build_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", contents=prompt
    )

    return response.text


def answer_question(document_id: str, question: str):
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
