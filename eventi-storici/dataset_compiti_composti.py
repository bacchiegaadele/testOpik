import opik

# inizializzazione di Opik
client = opik.Opik()
# creazione del dataset
dataset = client.get_or_create_dataset(name="Eventi_Storici_Composti")

# apertura del file con il contesto
with open("testi_no_ordine.txt", "r", encoding="utf-8") as f:
    context_text = f.read()

# definizione delle domande
domande_recap = [
    {
        "input": "Riordina i testi in ordine cronologico. Poi per ogni testo estrai il paese coinvolto in quell'evento.",
        "expected_output" : None
    },
    {
        "input": "Per tutti i nomi di persona citati nel testo, Identifica chi tra loro ha compiuto un 'colpo di Stato' e chi invece ha avviato un 'programma di ricerca segreto'.",
        "expected_output" : None
    },
    {
        "input": "Per ogni testo in cui si parla di un crollo, specifica se si tratta di un crollo fisico, economico o politico.",
        "expected_output" : None
    }
]

# inserimento nel Dataset
dataset.insert([
    {
        "input": item["input"],
        "expected_output": item["expected_output"],
        "context": context_text
    }
    for item in domande_recap
])

print(f"Dataset caricato! Vai su Opik per vedere le {len(domande_recap)} domande.")