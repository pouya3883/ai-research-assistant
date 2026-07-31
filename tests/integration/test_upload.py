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


def test_upload_rejects_invalid_pdf(client) -> None:
    invalid_pdf = Path("tests/data/invalid.pdf")

    with invalid_pdf.open("rb") as file:
        response = client.post(
            "/upload", files={"file": ("invalid.pdf", file, "application/pdf")}
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or corrupted PDF file"}

    assert not any(Path("data/uploads").glob("*invalid.pdf"))
    assert response.headers["content-type"].startswith("application/json")
