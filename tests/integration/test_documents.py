def test_get_documents_returns_document_list(client) -> None:
    response = client.get("/documents")

    assert response.status_code == 200

    documents = response.json()

    assert isinstance(documents, list)

    if documents:
        document = documents[0]

        assert isinstance(document["document_id"], str)
        assert isinstance(document["filename"], str)
        assert isinstance(document["characters"], int)
        assert isinstance(document["chunks"], int)


def test_get_document_returns_404_for_unknown_document(client) -> None:
    response = client.get("/documents/document_id")

    assert response.status_code == 404
    assert response.json() == {"detail": "Document not found"}
