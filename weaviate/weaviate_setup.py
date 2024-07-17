import weaviate

def setup_weaviate():
    client = weaviate.Client("http://localhost:8080")

    schema = {
        "classes": [
            {
                "class": "Document",
                "description": "A class for storing medical papers",
                "properties": [
                    {
                        "name": "title",
                        "dataType": ["string"]
                    },
                    {
                        "name": "content",
                        "dataType": ["text"]
                    }
                ]
            }
        ]
    }

    existing_classes = client.schema.get()["classes"]
    if not any(cls["class"] == "Document" for cls in existing_classes):
        client.schema.create(schema)

    return client
