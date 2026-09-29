import opik

# contesto
tabella_context = {
  "lunedì" :{
    "8:00": "CHIMICA",
    "9:00": "",
    "10:00": "FISICA MATEMATICA",
    "11:00": "",
    "12:00": "LETTERATURA INGLESE",
    "13:00": "",
    "14:00": "",
    "15:00": "LOGICA MATEMATICA",
    "16:00": "",
    "17:00": "",
    "18:00": ""
  },
  "martedì":{
    "8:00": "",
    "9:00": "LOGICA MATEMATICA",
    "10:00": "",
    "11:00": "",
    "12:00": "",
    "13:00": "FISICA MATEMATICA",
    "14:00": "",
    "15:00": "",
    "16:00": "",
    "17:00": "LETTERATURA ITALIANA",
    "18:00": ""
  },
  "mercoledì":{
    "8:00": "",
    "9:00": "",
    "10:00": "CHIMICA",
    "11:00": "",
    "12:00": "",
    "13:00": "GEOMETRIA",
    "14:00": "",
    "15:00": "LETTERATURA INGLESE",
    "16:00": "",
    "17:00": "",
    "18:00": ""
  },
  "giovedì":{
    "8:00": "FISICA MATEMATICA",
    "9:00": "",
    "10:00": "",
    "11:00": "",
    "12:00": "LETTERATURA ITALIANA",
    "13:00": "",
    "14:00": "",
    "15:00": "GEOMETRIA",
    "16:00": "",
    "17:00": "",
    "18:00": ""
  },
  "venerdì":{
    "8:00": "GEOMETRIA",
    "9:00": "",
    "10:00": "LOGICA MATEMATICA",
    "11:00": "",
    "12:00": "",
    "13:00": "",
    "14:00": "",
    "15:00": "",
    "16:00": "CHIMICA",
    "17:00": "",
    "18:00": ""
  }
}

# inizializzazione di Opik
client = opik.Opik()
# creazione del dataset
dataset = client.get_or_create_dataset(name="Orario_Settimanale_Lezioni")

# definizione delle domande
domande_recap = [
    {
        "input": "Quando c'è lezione di letteratura italiana?",
        "expected_output": "martedì alle 17:00, giovedì alle 12:00",
    },
    {
        "input": "Quando c'è lezione di matematica?",
        "expected_output": "lunedì alle 10:00 e alle 15:00, martedì alle 9:00 e alle 13:00, mercoledì alle 13:00, giovedì alle 8:00 e alle 15:00, venerdì alle 8:00 e alle 10:00",
    },
    {
        "input": "Che lezioni ci sono il mercoledì?",
        "expected_output": "chimica, geometria e letteratura inglese",
    },
    {
        "input": "In che giorni c'è lezione alle 15:00?",
        "expected_output": "lunedì, mercoledì e giovedì",
    },
    {
        "input": "In che giorno ci sono più lezioni?",
        "expected_output": "lunedì",
    },
    {
        "input": "In che giorno ci sono meno lezioni?",
        "expected_output": "martedì, mercoledì, giovedì e venerdì",
    }
]

# inserimento nel Dataset
dataset.insert([
    {
        "input": item["input"],
        "expected_output": item["expected_output"],
        "context": tabella_context
    }
    for item in domande_recap
])

print(f"Dataset caricato! Vai su Opik per vedere le {len(domande_recap)} domande.")