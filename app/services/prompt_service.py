def build_prompt(question: str, contexts: list[str]):
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

    return prompt
