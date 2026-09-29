import json
import opik

# caricamento del file JSON
with open('tabella-treni.json', 'r') as f:
    dati_tabella = json.load(f)
# conversione del JSON in stringa leggibile e indent=2 lo rende più facile da leggere per LLM
tabella_context = json.dumps(dati_tabella, indent=2)

# inizializzazione di Opik
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Orario_Giornaliero_Treni")

# definizione delle domande
domande_recap = [
    {
        "input": "Quali treni partono dal binario 2?",
        "expected_output": "Italo per Milano alle 8:35 e Regionale per Verona alle 10:00",
    },
    {
        "input": "Che treni ci sono per Rovigo?",
        "expected_output": "Regionale alle 9:03 al binario 3 e Regionale alle 10:11 al binario 5",
    },
    {
        "input": "Che treni partono tra le 9:30 e le 10:00?",
        "expected_output": "Italo per Roma alle 9:38 al binario 3, Frecciarossa per Venezia alle 9:42 al binario 1, Regionale per Bologna alle 9:55 al binario 1 e Regionale per Verona alle 10:00 al binario 2",
    },
    {
        "input": "Supponendo siano le 9:00, quand'è il prossimo treno per Venezia?",
        "expected_output": "Italo alle 9:12 al binario 3",
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