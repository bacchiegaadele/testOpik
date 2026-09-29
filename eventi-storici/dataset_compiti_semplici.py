import opik

# inizializzazione Opik
client = opik.Opik()
# creazione del dataset
dataset = client.get_or_create_dataset(name="Eventi_Storici")

# apertura del file con il contesto
with open("testi.txt", "r", encoding="utf-8") as f:
    context_text = f.read()

# definizione delle domande
domande_recap = [
    {
        "input": "In quali testi si parla di un crollo?",
        "expected_output": "rivoluzione francese, crollo della borsa di Wall Street e crollo del muro di Berlino",
    },
    {
        "input": "In quale testo viene citata la Seconda Guerra Mondiale?",
        "expected_output": "bomba atomica su Hiroshima",
    },
    {
        "input": "Cosa successe nel 1799?",
        "expected_output": "colpo di Stato di Napoleone Bonaparte",
    },
    {
        "input": "Fai un riassunto del secondo testo di circa 50 parole.",
        "expected_output": None,
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