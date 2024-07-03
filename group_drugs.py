import pandas as pd
from collections import defaultdict

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

for chemicals, drugs in drug_groups.items():
    print(f"Chemicals: {chemicals}")
    print("Drugs:", ", ".join(drugs))
    print()
