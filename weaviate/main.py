import os
from data_loader import load_text_files
from weaviate_setup import setup_weaviate
from data_uploader import upload_data_to_weaviate
from rag_model import initialize_retriever, initialize_generator, generate_response

directory = "/home/pes1ug22am100/Documents/Summer '24/Summer Research/PMC000xxxxxx"

def main():
    text_data = load_text_files(directory)

    client = setup_weaviate()

    upload_data_to_weaviate(client, text_data)

    retriever = initialize_retriever(client)
    generator = initialize_generator()

    query = "What are the side effects of dolo 650?"
    response = generate_response(query, retriever, generator)
    print(response)

if __name__ == "__main__":
    main()
