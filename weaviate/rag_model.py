import weaviate
from transformers import pipeline

def initialize_retriever(client):
    def retrieve(query, limit=5):
        result = client.query.get("Document", ["title", "content"]) \
            .with_near_text({"concepts": [query]}) \
            .with_limit(limit) \
            .do()
        return result["data"]["Get"]["Document"]
    
    return retrieve

def initialize_generator():
    return pipeline('text-generation', model='gpt-2')

def generate_response(query, retriever, generator):
    documents = retriever(query)
    context = " ".join(doc["content"] for doc in documents)
    result = generator(query + context, max_length=200)
    
    return result[0]["generated_text"]
