import opik

# inizializzazione di Opik
client = opik.Opik()
dataset = client.get_or_create_dataset(name="Testi_Multipli_Montagne2")

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
        "input": "Sulla base dei rilievi di dicembre 2025, qual è l'esatta differenza altimetrica tra la calotta ghiacciata sommitale e la cima rocciosa sottostante sul Monte Bianco? A) 11,23 metri. B) 15,3 metri. C) 23 metri. D) 17,07 metri.",
        "expected_output": "B",
    },
    {
        "input": "Quale specifica teoria scientifica fu verificata sperimentalmente durante la spedizione di Horace-Bénédict de Saussure del 1787? A) La misurazione dell'altezza esatta di 4.809,07 m mediante l'uso di barometri. B) L'effetto del paradosso glaciologico sull'accumulo di neve sopra i 4.000 metri. C) La datazione dell'orogenesi ercinica nel nucleo granitico del massiccio. D) La teoria di Torricelli sulla pressione atmosferica attraverso l'uso di igrometri e barometri.",
        "expected_output": "D",
    },
    {
        "input": "Secondo le analisi onomastiche fornite, quale radice linguistica suggerisce che il Monte Rosa sia il bacino imbrifero primario che 'tiene capo' al sistema idrografico? A) Il termine latino rosia, che indica la presenza di ghiacci perenni. B) Il termine dialettale valdostano rouése o rouja. C) La radice ebraica RoSa. D) Il toponimo leonardesco Monboso riferito all'architettura fisica.",
        "expected_output": "C",
    },
    {
        "input": "In quale ordine cronologico corretto sono avvenute le seguenti tappe storiche del Monte Rosa? A) Raggiungimento della Roccia della Scoperta; Conquista della Punta Gnifetti; Ridenominazione della Punta Dufour; Ascesa di Achille Ratti. B) Conquista di Pietro Giordani; Raggiungimento della Roccia della Scoperta; Spedizione di Charles Hudson; Istituzione del parco naturale dell'Alta Val Sesia. C) Conquista della Punta Gnifetti; Ridenominazione della Punta Dufour; Spedizione di Charles Hudson; Ascesa della Parete Est. D) Transito dei Walser; Raggiungimento della Roccia della Scoperta; Conquista di Pietro Giordani; Conquista della Punta Gnifetti.",
        "expected_output": "D",
    },
    {
        "input": "Quale dettaglio relativo alla tragedia del 1865 è riportato come un 'vuoto perenne' nella storia del Cervino? A) La rottura della corda che causò la caduta mortale di quattro alpinisti. B) Il recupero dei corpi di Croz, Hadow e Hudson sul ghiacciaio del Matterhorn. C) Il fatto che il corpo di Lord Francis Douglas non sia mai stato ritrovato. D) La perdita della documentazione scientifica di Whymper sulla geomorfologia.",
        "expected_output": "C",
    },
    {
        "input": "Il Grand Combin comprende quattro vette sopra i 4.000 metri. Qual è l'ordine corretto di altezza decrescente per le tre vette secondarie? A) Aiguille du Croissant, Combin de la Tsessette, Combin de Valsorey. B) Combin de Grafeneire, Combin de Valsorey, Aiguille du Croissant. C) Combin de la Tsessette, Aiguille du Croissant, Combin de Valsorey. D) Aiguille du Croissant, Combin de Valsorey, Combin de la Tsessette.",
        "expected_output": "D",
    },
    {
        "input": "Perché il passaggio denominato 'Le Corridor' è descritto come un pericolo oggettivo estremo? A) Per la pendenza elevata che impedisce l'accumulo di neve stabilizzata. B) Perché è costantemente minacciato dal crollo di seracchi pensili provenienti dal bacino sommitale. C) A causa della scarsa visibilità dovuta alla divergenza delle creste parallele. D) Perché si trova alla quota strategica di 3.658 m dove la ritirata è complessa.",
        "expected_output": "B",
    },
    {
        "input": "Quale distinzione tecnica rende il Finsteraarhorn superiore a tutte le altre vette svizzere, pur essendo solo la nona delle Alpi? A) L'altezza di 4.274 metri che lo rende il punto più alto del Cantone Vallese. B) La sua posizione come unico punto culminante del bacino del Rodano. C) Un isolamento di 51,7 km misurato rispetto al massiccio del Monte Rosa. D) Una prominenza di 2.279 metri, la più alta della Svizzera.",
        "expected_output": "D",
    },
    {
        "input": "Quale di questi dati tecnici del Gran Paradiso è errato secondo i parametri identificativi forniti? A) Coordinata Nord: 45°31′07.02″. B) Isolamento: 45,1 km. C) Prominenza: 1.512 m. D) Altezza: 4.061,20 m s.l.m.",
        "expected_output": "C",
    },
    {
        "input": "Chi detiene il record di velocità per il percorso Le Pont-Vetta e ritorno, e in quale anno è stato stabilito? A) Nadir Maguet nel 2013 con il tempo di 2h 02' 32''. B) Kilian Jornet nel 2013 con il tempo di 2h 52' 02''. C) Joseph-Marie Henry nel 1931 con l'asino Cagliostro. D) Nadir Maguet nel 2020 con il tempo di 2h 02' 32''.",
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