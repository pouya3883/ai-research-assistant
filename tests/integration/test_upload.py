from pathlib import Path


def test_upload_pdf_returns_document_metadata(client) -> None:
    sample_pdf = Path("tests/data/sample.pdf")

    with sample_pdf.open("rb") as file:
        response = client.post(
            "/upload", files={"file": ("sample.pdf", file, "application/pdf")}
        )

    assert response.status_code == 200

    document = response.json()

    assert isinstance(document["document_id"], str)
    assert document["filename"] == "sample.pdf"
    assert isinstance(document["characters"], int)
    assert isinstance(document["chunks"], int)

    # cleanup
    delete_response = client.delete(f"/documents/{document['document_id']}")

    assert delete_response.status_code == 200
