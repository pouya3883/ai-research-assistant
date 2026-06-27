from app.services.document_registry import delete_document as delete_document_metadata
from app.services.chunk_service import delete_document_chunks
from app.services.vector_store import delete_document_embeddings
from app.services.storage_service import delete_files, UPLOADS_DIR, PROCESSED_DIR


def delete_document(document_id: str) -> bool:
    delete_files(UPLOADS_DIR, document_id=document_id)

    delete_files(PROCESSED_DIR, document_id=document_id)

    delete_document_chunks(document_id=document_id)

    delete_document_embeddings(document_id=document_id)

    return delete_document_metadata(document_id=document_id)
