from app.config.settings import settings
from app.retrieval.openai_embeddings import OpenAIEmbeddingProvider


provider = OpenAIEmbeddingProvider(settings=settings)
vectors = provider.embed_texts(
    [
        "Python is a programming language.",
        "Docker packages applications into containers.",
    ]
)

print(f"Number of vectors: {len(vectors)}")
print(f"Vector dimension: {len(vectors[0])}")
