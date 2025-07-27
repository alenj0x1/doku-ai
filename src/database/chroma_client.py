import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import config

chroma_client = chromadb.HttpClient(
    host=config.CHROMADB_HOST,
    port=config.CHROMADB_PORT,
)
chroma_client.heartbeat()

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

contexts = chroma_client.get_or_create_collection(
    name="contexts", embedding_function=embedding_fn
)
