import opik

# inizializzazione di Opik
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Test_Metadata")

def load_context(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Errore: Il file non è stato trovato.")
        return None
    
# caricamento del file di testo come contesto
context_text = load_context("testi.txt")

# definizione delle domande
domande_recap = [
    {
        "input": "Quale episodio della Seconda Guerra Mondiale è menzionato nel testo riguardo al Monte Bianco? A. La costruzione di una stazione meteorologica militare sulla vetta. B. Gli scontri tra truppe alpine al Rifugio Torino e al Col du Midi. C. Il bombardamento della funivia del Monte Bianco. D. L’occupazione della vetta da parte di truppe tedesche.",
        "expected_output": "B",
        "metrics" : ["contains_m", "exact_match_m", "valid_option_m", "single_answer_m"]
    },
    {
        "input": "Quale struttura si trova sulla Punta Gnifetti? A. Il rifugio Vittorio Emanuele II. B. La Capanna di Panossière. C. La Capanna Regina Margherita. D. Il Rifugio Torino.",
        "expected_output": "C",
        "metrics" : ["contains_m", "exact_match_m"]
    },
    {
        "input": "Quale cresta fu utilizzata da Edward Whymper per la prima ascensione del 1865? A. Cresta del Leone. B. Cresta Zmutt. C. Cresta Furggen. D. Cresta dell’Hörnli.",
        "expected_output": "D",
        "metrics" : ["valid_option_m", "single_answer_m"]
    },
    {
        "input": "Qual è il valore di prominenza del Finsteraarhorn? A. 2.179 m. B. 2.297 m. C. 2.279 m. D. 2.279,5 m.",
        "expected_output": "C",
        "metrics" : ["contains_m"]
    }
]

# inserimento nel Dataset
dataset.insert([
    {
        "input": item["input"],
        "expected_output": item["expected_output"],
        "context": context_text,
        "metadata": {
            "metrics": item["metrics"]
        }
    }
    for item in domande_recap
])

print(f"Dataset caricato! Vai su Opik per vedere le {len(domande_recap)} domande.")