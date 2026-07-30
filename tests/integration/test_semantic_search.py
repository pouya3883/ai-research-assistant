from pathlib import Path


def test_semantic_search_returns_relevant_results(client) -> None:
    sample_pdf = Path("tests/data/sample.pdf")

    with sample_pdf.open("rb") as file:
        upload_response = client.post(
            "/upload", files={"file": ("sample.pdf", file, "application/pdf")}
        )

    assert upload_response.status_code == 200

    document = upload_response.json()
    document_id = document["document_id"]

    response = client.get(
        f"/documents/{document_id}/semantic-search",
        params={"query": "large language models"},
    )

    assert response.status_code == 200

    results = response.json()

    assert isinstance(results, list)
    assert len(results) > 0

    first_result = results[0]

    assert first_result["document_id"] == document_id
    assert isinstance(first_result["filename"], str)
    assert isinstance(first_result["chunk_index"], int)
    assert isinstance(first_result["total_chunks"], int)
    assert isinstance(first_result["content"], str)
    assert isinstance(first_result["score"], float)

    delete_response = client.delete(f"/documents/{document_id}")

    assert delete_response.status_code == 200
