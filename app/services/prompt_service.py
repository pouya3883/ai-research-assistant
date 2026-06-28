from app.models.retrieval import RetrievalResult


def build_prompt(question: str, retrieval: RetrievalResult):
    numbered_contexts = []

    for index, chunk in enumerate(retrieval.results, start=1):
        numbered_contexts.append(f"[{index}]\n{chunk.content}")

    context = "\n\n".join(numbered_contexts)

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer in English.

    Use only the provided context.

    When you use information from the context, cite the corresponding context number in square brackets, for example: [1] or [2].

    If the context is written in another language, translate the relevant information to English before answering.
    """

    return prompt
