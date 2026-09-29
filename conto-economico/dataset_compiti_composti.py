#importazione delle librerie necessarie
import json
import opik

#caricamento del contesto attraverso un file JSON
with open('conto-economico.json', 'r') as f:
    dati_tabella = json.load(f)
#converte il JSON in una stringa leggibile
#indent=2 lo rende più facile da leggere per l'LLM
tabella_context = json.dumps(dati_tabella, indent=2)

#inizializzione di Opik e creazione del dataset
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Conto_Economico_2024_2025")

#definizione delle domande attraverso un dizionario
domande_recap = [
    {
        "input": "Se nei costi di produzione(B) del 2024 applicassi uno sconto sui servizi (7) del 20%, come cambierebbe il totale dei costi di produzione e la differenza tra valore e costi di produzione?",
        "expected_output": None,
    },
    {
        "input": "Se nel 2025 il totale del valore della produzione (A) aumentasse del 10% ma contemporaneamente i costi per materie prime (6) aumentassero del 5%, quale sarebbe il nuovo risultato della differenza tra valore e costi di produzione?",
        "expected_output": None,
    },
    {
        "input": "Per ogni voce della sezione C sia del 2024 che del 2025, controntale singolarmente e tutte assieme.",
        "expected_output": None,
    }
]

#inserimento delle domande nel dataset
dataset.insert([
    {
        "input": item["input"],
        "expected_output": item["expected_output"],
        "context": tabella_context  #inietta il JSON della tabella come contesto
    }
    for item in domande_recap
])

print(f"Dataset caricato! Vai su Opik per vedere le {len(domande_recap)} domande.")