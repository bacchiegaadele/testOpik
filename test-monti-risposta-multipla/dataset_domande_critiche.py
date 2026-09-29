import opik

# inizializzazione di Opik
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Testi_Multipli_Montagne3")

# caricamento del file di testo come contesto
def load_context(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Errore: Il file non è stato trovato.")
        return None
context_text = load_context("testi.txt")

# definizione delle domande
domande_recap = [
    {
        "input": "Identifica l'errore tecnico presente in questa descrizione del Gran Paradiso basata sui dati forniti nel testo: 'Il Gran Paradiso (4.061,20 m) presenta una prominenza di 1.512 m e un isolamento di 45,1 km, fungendo da spartiacque tra Valsavarenche e Val di Cogne.' A) L'altezza corretta è 4.026 m, riferita al Roc. B) Lo spartiacque corretto è tra la Valle Anzasca e la Valsesia. C) La prominenza indicata è errata, essendo in realtà di 1.888 m. D) L'isolamento è errato, essendo in realtà di 51,7 km.",
        "expected_output": "C",
    },
    {
        "input": "Quale delle seguenti sequenze rappresenta correttamente l’ordine di altezza crescente tra queste cime alpine? A. Grand Combin, Gran Paradiso, Monte Rosa, Monte Bianco. B. Gran Paradiso, Gran Combin, Monte Bianco, Monte Rosa. C. Monte Bianco, Monte Rosa, Grand Combin, Gran Paradiso. D. Gran Paradiso, Gran Combin, Monte Rosa, Monte Bianco.",
        "expected_output": "D",
    },
    {
        "input": "Nel testo viene menzionata la costruzione di una piramide di pietra sulla vetta del Finsteraarhorn nel 1829. Qual era lo scopo principale di questa struttura? A. Servire come punto di osservazione astronomica. B. Segnalare un punto trigonometrico per misurazioni geografiche. C. Commemorare la prima ascensione della montagna. D. Il testo non lo specifica.",
        "expected_output": "D",
    },
    {
        "input": "Quale delle seguenti sequenze rappresenta correttamente l’ordine cronologico degli eventi legati al Monte Bianco? A. Prime misurazioni moderne, spedizione scientifica di Saussure, prima ascensione. B. Prima ascensione, prime misurazioni moderne, spedizione scientifica di Saussure. C. Prima ascensione, spedizione scientifica di Saussure, prime misurazioni moderne. D. Il testo non lo specifica.",
        "expected_output": "C",
    },
    {
        "input": "Quale dei seguenti elementi storici è associato alla presenza dei Walser nell’area del Monte Bianco? A. Lo sviluppo dell’alpinismo scientifico. B. L’insediamento di comunità alpine con una propria lingua e cultura. C. La costruzione delle prime funivie alpine. D. Il testo non lo specifica.",
        "expected_output": "D",
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