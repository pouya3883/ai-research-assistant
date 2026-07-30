from pathlib import Path


def test_delete_document_removes_existing_document(client) -> None:
    sample_pdf = Path("tests/data/sample.pdf")

    with sample_pdf.open("rb") as file:
        upload_response = client.post(
            "/upload", files={"file": ("sample.pdf", file, "application/pdf")}
        )

    assert upload_response.status_code == 200

    document = upload_response.json()
    document_id = document["document_id"]

    delete_response = client.delete(f"/documents/{document_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Document deleted"}

    get_response = client.get(f"/documents/{document_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Document not found"}
