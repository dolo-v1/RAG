import weaviate

def upload_data_to_weaviate(client, text_data):
    for file_name, content in text_data.items():
        client.data_object.create(
            data_object={
                "title": file_name,
                "content": content
            },
            class_name="Document"
        )
