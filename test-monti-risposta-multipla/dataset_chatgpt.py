import opik

# inizializzazione di Opik
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Testi_Multipli_Montagne")
    
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
        "input": "Quale episodio della Seconda Guerra Mondiale è menzionato nel testo riguardo al Monte Bianco? A. La costruzione di una stazione meteorologica militare sulla vetta. B. Gli scontri tra truppe alpine al Rifugio Torino e al Col du Midi. C. Il bombardamento della funivia del Monte Bianco. D. L’occupazione della vetta da parte di truppe tedesche.",
        "expected_output": "B",
    },
    {
        "input": "Quale struttura si trova sulla Punta Gnifetti? A. Il rifugio Vittorio Emanuele II. B. La Capanna di Panossière. C. La Capanna Regina Margherita. D. Il Rifugio Torino.",
        "expected_output": "C",
    },
    {
        "input": "Quale cresta fu utilizzata da Edward Whymper per la prima ascensione del 1865? A. Cresta del Leone. B. Cresta Zmutt. C. Cresta Furggen. D. Cresta dell’Hörnli.",
        "expected_output": "D",
    },
    {
        "input": "Qual è il valore di prominenza del Finsteraarhorn? A. 2.179 m. B. 2.297 m. C. 2.279 m. D. 2.279,5 m.",
        "expected_output": "C",
    },
    {
        "input": "Quale ghiacciaio del Gran Paradiso domina il versante orientale del massiccio? A. Ghiacciaio del Gran Paradiso. B. Ghiacciaio del Laveciau. C. Ghiacciaio della Tribolazione. D. Ghiacciaio del Miage.",
        "expected_output": "C",
    },
    {
        "input": "Quale elemento geografico spiega perché la Parete Est di Macugnaga abbia storicamente isolato l’omonimo villaggio? A. Il dislivello superiore ai duemila metri della parete orientale. B. La presenza di un ghiacciaio permanente che blocca i passaggi. C. La mancanza di valichi tra le valli circostanti. D. L’orientamento della parete verso nord che impedisce la fusione del ghiaccio.",
        "expected_output": "A",
    },
    {
        "input": "Il Finsteraarhorn è identificato nel testo come punto culminante di un importante sistema idrografico. Quale? A. Il bacino del Rodano. B. Il bacino del Po. C. Il bacino del Danubio. D. Il bacino del Reno.",
        "expected_output": "D",
    },
    {
        "input": "Quale elemento storico è direttamente collegato alla conservazione dello stambecco alpino nel massiccio del Gran Paradiso? A. L’istituzione di un santuario naturale medievale. B. La creazione della Riserva Reale di Caccia nel XIX secolo. C. Il divieto di caccia imposto dal Parco Nazionale Svizzero. D. La presenza di ghiacciai che impedivano la caccia.",
        "expected_output": "B",
    },
    {
        "input": "Quale materiale specifico fu utilizzato per costruire la piramide di pietra eretta sulla vetta del Finsteraarhorn nel 1829? A. Blocchi di granito locale. B. Lastre di gneiss. C. Pietre raccolte lungo la cresta sommitale. D. Il testo non lo specifica.",
        "expected_output": "D",
    },
    {
        "input": "Quale massiccio è descritto sia come bacino idrografico importante sia come luogo dove un passaggio glaciale costituisce un grave rischio alpinistico? A. Monte Bianco. B. Monte Rosa. C. Grand Combin. D. Gran Paradiso.",
        "expected_output": "C",
    },
    {
        "input": "Quale delle seguenti montagne presenta la maggiore prominenza secondo i dati riportati nel testo? A. Monte Bianco. B. Gran Paradiso. C. Grand Combin. D. Finsteraarhorn.",
        "expected_output": "D",
    },
    {
        "input": "Quale montagna del testo è descritta come caratterizzata da una struttura piramidale isolata con quattro pareti orientate secondo i punti cardinali? A. Monte Rosa. B. Cervino. C. Grand Combin. D. Finsteraarhorn.",
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