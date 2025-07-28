from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from typing import Optional, List, Dict
from pymupdf import Document
from langchain_core.vectorstores import VectorStoreRetriever


class ChromaManager:
    embed_model: FastEmbedEmbeddings
    persist_directory: str

    def __init__(self, persist_directory: str):
        self.embed_model = FastEmbedEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.persist_directory = persist_directory

    def insert_document(
        self,
        chunks: list[Document],
        collection_name: str,
        ids: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Chroma:
        # Validate ids length if is not none
        if ids is not None and len(ids) is not len(chunks):
            raise ValueError("incorrect ids length")

        # Set metadata in all chunks
        if metadata:
            for chunk in chunks:
                chunk.metadata.update(metadata)

        return Chroma.from_documents(
            ids=ids,
            documents=chunks,
            embedding=self.embed_model,
            persist_directory=self.persist_directory,
            collection_name=collection_name,
        )

    def get_documents(
        self,
        collection_name: str,
        id: Optional[str] = None,
        where: Optional[Dict] = None,
        limit: Optional[int] = 10,
    ) -> dict[str, any]:
        vector_store = self.vector_store(collection_name=collection_name)

        if id:
            return vector_store.get(ids=[id], limit=limit)
        if where:
            return vector_store.get(where=where, limit=limit)

        return {}

    def retriever(
        self, collection_name: str, search_kwargs: dict = {}
    ) -> VectorStoreRetriever:
        return self.vector_store(collection_name=collection_name).as_retriever(
            search_kwargs=search_kwargs
        )

    def remove_document(
        self,
        collection_name: str,
        id: Optional[str] = None,
        where: Optional[Dict] = None,
    ):
        vector_store = self.vector_store(collection_name=collection_name)

        if id:
            vector_store.delete(ids=[id])
        elif where:
            vector_store.delete(where=where)
        else:
            raise ValueError("id and metadata missing value")

    def vector_store(self, collection_name: str) -> Chroma:
        return Chroma(
            embedding_function=self.embed_model,
            persist_directory=self.persist_directory,
            collection_name=collection_name,
        )
