from pyArango.connection import *
import pandas as pd

def drop_collection(db, collection_name):
    if db.hasCollection(collection_name):
        db[collection_name].delete()
        print(f"Collection '{collection_name}' dropped successfully.")
    else:
        print(f"Collection '{collection_name}' does not exist.")

def truncate_collection(collection):
    num_deleted = collection.truncate()
    print(f"{num_deleted} documents deleted from collection.")

try:
    conn = Connection(username="root", password="namita", arangoURL="http://localhost:8529")
    db = conn["_system"]

    drop_collection(db, 'drugs') 
    drop_collection(db, 'adjacency')  

    df = pd.read_csv('/home/pes1ug22am100/Documents/Summer Research/final-output.csv')

    if not db.hasCollection('drugs'):
        drugs_collection = db.createCollection(name="drugs")
    else:
        drugs_collection = db["drugs"]

    if not db.hasCollection('adjacency'):
        adjacency_collection = db.createCollection(name="adjacency", edge=True)
    else:
        adjacency_collection = db["adjacency"]

    for index, row in df.iterrows():
        drug = {
            '_key': str(index),
            'name': row['Drug name'],
            'chemical': row['chemical']
        }
        try:
            doc = drugs_collection.createDocument(drug)
            doc.save()
            print(f"Document saved successfully for drug: {drug['name']}")
        except CreationError as e:
            print(f"Error saving document for drug: {drug['name']}. Error: {e}")

    #Assuming adjacency relationships based on drug name similarity
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if df.iloc[i]['Drug name'] != df.iloc[j]['Drug name']:
                # Get document keys
                key_i = drugs_collection[str(i)]._key
                key_j = drugs_collection[str(j)]._key
                edge = {
                    '_from': f"drugs/{key_i}",
                    '_to': f"drugs/{key_j}",
                    'type': 'similar_drug'
                }
                try:
                    adj_edge = adjacency_collection.createEdge(edge)
                    adj_edge.save()
                    print(f"Edge saved successfully between {edge['_from']} and {edge['_to']}")
                except CreationError as e:
                    print(f"Error saving edge between {edge['_from']} and {edge['_to']}. Error: {e}")

except ConnectionError as e:
    print(f"Failed to connect to ArangoDB. Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
