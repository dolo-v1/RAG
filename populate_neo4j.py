import pandas as pd
from collections import defaultdict
from neo4j import GraphDatabase

class DrugGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_drug(self, drug_name):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_drug, drug_name)

    def create_chemical(self, chemical_name):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_chemical, chemical_name)

    def create_relationship(self, drug_name, chemical_name):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_relationship, drug_name, chemical_name)

    @staticmethod
    def _create_and_return_drug(tx, drug_name):
        query = "MERGE (d:Drug {name: $drug_name}) RETURN d"
        tx.run(query, drug_name=drug_name)

    @staticmethod
    def _create_and_return_chemical(tx, chemical_name):
        query = "MERGE (c:Chemical {name: $chemical_name}) RETURN c"
        tx.run(query, chemical_name=chemical_name)

    @staticmethod
    def _create_and_return_relationship(tx, drug_name, chemical_name):
        query = (
            "MATCH (d:Drug {name: $drug_name}), (c:Chemical {name: $chemical_name}) "
            "MERGE (d)-[:CONTAINS]->(c)"
        )
        tx.run(query, drug_name=drug_name, chemical_name=chemical_name)

df = pd.read_csv('/home/pes1ug22am100/Documents/Summer Research/final-output.csv')

def normalize_chemicals(chemicals):
    chemicals = [chem.strip() for chem in chemicals.split('+')]
    return ' + '.join(sorted(chemicals))

drug_groups = defaultdict(list)

for _, row in df.iterrows():
    drug_name = str(row['Drug name'])
    chemicals = str(row['chemical'])
    normalized_chemicals = normalize_chemicals(chemicals)
    drug_groups[normalized_chemicals].append(drug_name)

uri = "bolt://localhost:7687"
user = "neo4j"
password = "Neo4j"

graph = DrugGraph(uri, user, password)

for chemicals, drugs in drug_groups.items():
    #chemical nodes
    for chemical in chemicals.split(' + '):
        graph.create_chemical(chemical)
    #drug nodes and relationships
    for drug in drugs:
        graph.create_drug(drug)
        for chemical in chemicals.split(' + '):
            graph.create_relationship(drug, chemical)

graph.close()
