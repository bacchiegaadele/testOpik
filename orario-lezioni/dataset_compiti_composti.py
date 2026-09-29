import json
import opik

# caricamento del file JSON
with open('orario-settimanale.json', 'r') as f:
    dati_tabella = json.load(f)
# conversione del JSON in stringa leggibile e indent=2 lo rende più facile da leggere per LLM
tabella_context = json.dumps(dati_tabella, indent=2)

# inizializzazione di Opik
client = opik.Opik()
# creazione del dataset
dataset = client.get_or_create_dataset(name="Orario_Lezioni_compiti_composti")

# definizione delle domande
domande_recap = [
    {
        "input": "Seleziona martedì, giovedì e venerdì nella settimana.  Poi dimmi in quei giorni quando c'è geometria.",
        "expected_output": "giovedì alle 15:00 e venerdì alle 8:00",
    },
    {
        "input": "Fammi una tabella con le lezioni pomeridiane, dalle 13:00 in poi. In che giorni c'è una lezione sola al pomeriggio?",
        "expected_output": "lunedì, giovedì e venerdì",
    },
    {
        "input": "Seleziona i giorni in cui c'è lezione di chimica. In questi giorni quando non c'è anche lezione di letteratura?",
        "expected_output": "venerdì",
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