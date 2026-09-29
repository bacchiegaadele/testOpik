import opik

# inizializzazione di Opik
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Testi_Montagne")

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
        "input": "Il testo menziona spedizioni scientifiche ottocentesche dedicate allo studio dei ghiacciai alpini. Quali istituzioni le finanziavano?",
        "expected_output": "testo non specifica",
    },
    {
        "input": "Il testo menziona un dualismo geomorfologico in una montagna, individua di quale si tratta e spiega questo dualismo.",
        "expected_output": "Grand Combin",
    },
    {
        "input": "Fammi una tabella comparativa di tutti i monti mettendoli in ordine di altezza crescente, per ogni monte nella tabella metti: nome, altezza, stati in cui è situato, anno della prima ascensione, autore della prima ascensione.",
        "expected_output": None,
    },
    {
        "input": "Individua due montagne del testo che presentano caratteristiche glaciali rilevanti e spiega in cosa differiscono.",
        "expected_output": "Monte Bianco e Grand Combin",
    },
    {
        "input": "Tra Monte Rosa, Gran Paradiso e Finsteraarhorn, quale è descritto come il più alto interamente situato in territorio svizzero o italiano? Motiva la risposta.",
        "expected_output": "Finsteraarhorn",
    },
    {
        "input": "Se la cima rocciosa del Monte Bianco si trova a 4.792 m e la copertura glaciale può raggiungere 23 metri, qual è l’altezza massima raggiunta dalla vetta ghiacciata?",
        "expected_output": "4807.3",
    },
    {
        "input": "Il Monte Bianco viene definito “cerniera orografica e politica”. Quale delle seguenti interpretazioni è più coerente con il testo? A) È una zona dove si incontrano diverse placche tettoniche; B) Ha avuto un ruolo nel definire confini e identità culturali europee; C) È il punto di collegamento tra i ghiacciai alpini; D) È il punto di passaggio delle principali rotte commerciali medievali",
        "expected_output": "B",
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