import json
import opik

# caricamento del file JSON
with open('tabella-treni2.json', 'r') as f:
    dati_tabella = json.load(f)
# conversione del JSON in stringa leggibile e indent=2 lo rende più facile da leggere per LLM
tabella_context = json.dumps(dati_tabella, indent=2)

# inizializzazione di Opik
client = opik.Opik()
# creazione del dataset
dataset = client.get_or_create_dataset(name="Orario_Treni_compiti_composti")

# definizione delle domande
domande_recap = [
    {
        "input": "Elenca i treni che partono dalle 9:00 alle 9:45. Quali treni vanno a Venezia? Tra questi quale ha durata minore?",
        "expected_output": "Frecciarossa per Venezia delle 9:42 al binario 1",
    },
    {
        "input": "Seleziona i treni che partono dal binario 3. C'è qualche Italo che parte da quel binario dopo le 9:30?",
        "expected_output": "Italo per Roma delle 9:38",
    },
    {
        "input": "Seleziona i treni che hanno durata maggiore di 2 ore. C'è qualche treno che va a Rovigo o a Verona?",
        "expected_output": "No",
    }
]

# inserimento nel Dataset
dataset.insert([
    {
        "input": item["input"],
        "expected_output": item["expected_output"],
        "context": tabella_context  # inietta il JSON della tabella come contesto
    }
    for item in domande_recap
])

print(f"Dataset caricato! Vai su Opik per vedere le {len(domande_recap)} domande.")