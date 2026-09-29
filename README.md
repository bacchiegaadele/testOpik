# **TEST DI VARI LLM SU OPIK**

## **INTRODUZIONE**
Questo progetto è relativo ad un periodo di tirocinio svolto presso l'azienda Zucchetti Spa a Padova della durata di 2 mesi.
Mi è stato assegnato questo progetto che prevedeva di testare degli LLM di varie dimensioni, da 1b a 30b, con compiti inizialmente più semplici e successivamente più complessi. Sono state prese in esame varie casistiche passando come contesto delle strutture tabellari o lunghi testi; per poi effettuare domande di varia natura sui dati, come: estrazione, logica, ragionamento, ecc.

Per realizzare questi esperimenti mi sono appoggiata dapprima a OpenWeb UI, un'interfaccia web self-hosted con funzionalità per gestione e interazione con LLMs, e successivamente ad Opik, riportato il codice Python in questo progetto.
Opik, di Comet, è una piattaforma open source di logging, debug e ottimizzazione per agenti di AI ed applicazioni LLM.
Ogni directory contiene una tipologia di test effettuati su contesti diversi e presenta la seguente struttura:
- context .json o .txt : per definire il contesto su cui fare le domande all’LLM;
- dataset.py : per creare il dataset, popolarlo e caricarlo sulla piattaforma Opik;
- evaluate.py : per creare e definire la fase di valutazione e per chiamare le metriche opportune.


## **INSTALLAZIONE E SET-UP LOCALE DI OPIK**
Per far girare questo progetto, è necessario avere un'istanza di Opik attiva localmente. La procedura di installazione richiede l'utilizzo di Docker per gestire i vari componenti della piattaforma.

### 1. Prerequisiti
Bisogna assicurarsi di aver installato i seguenti strumenti nel sistema:
- Git/GitHub: per clonare la repository ufficiale di Opik.
- Docker Desktop: per avviare i container della piattaforma.
- Python: per scrivere i progetti.

### 2. Installazione di Opik
Clona la repository di Opik con il comando:
```git clone https://github.com/comet-ml/opik.git```  
Per navigare nella cartella di Opik:
```cd opik/deployment/docker-compose```  
Per far partire la piattaforma di Opik con l'infrastruttura di Docker:
```docker compose up -d```  
Opik è ora disponibile su http://localhost:5173

### 3. Configurazione del progetto
Per utilizzare l'SDK Python di Opik con la tua istanza locale di Opik, dovrai eseguire nella directory del progetto questi 2 comandi:
- ```pip install opik```
- ```opik configure --use_local``` 

Mentre nel file python bisogna importare la libreria principale: ```import opik```


## **DATASET**
La struttura di base del file dataset.py è la seguente:
```python
# importo libreria principale di Opik per tracciamento e valutazione
import opik
# inizializzo client Opik per gestire connessione con server
client = opik.Opik()
# creo nuovo dataset
dataset = client.get_or_create_dataset(name="Mio_Dataset")
# funzione di utility per leggere file di testo che funge da contesto (opzionale)
def load_context(file_path):
    try:
        # apro file 'testi.txt' in lettura con codifica standard UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read() # ritorno intero contenuto del file
    except FileNotFoundError:
        # gestisco errore se file non è presente nel percorso indicato
        print("Errore: Il file non è stato trovato.")
        return None
# chiamo funzione precedentemente creata e salvo contesto
context_text = load_context("testi.txt")
# creo lista di dizionari che rappresentano casi di test (domanda, risposta attesa e metriche)
domande_recap = [
    {
        "input": "...", # domanda
        "expected_output": "...", # risposta corretta attesa
        "metrics" : ["m1", "m2"] # elenco metriche da applicare
    },
    {
        "input": "...", # domanda
        "expected_output": "...", # risposta corretta attesa
        "metrics" : "m3" # elenco metriche da applicare
    }
]
# ciclo per inserire i dati nel dataset
dataset.insert([
    {
        "input": item["input"], # carico domanda
        "expected_output": item["expected_output"], # carico risposta corretta
        "context": context_text, # carica contesto letto da file .txt
        "metadata": {
            "metrics": item["metrics"] # salvo nei metadati quali metriche attivare dopo
        }
    }
    for item in domande_recap
])
# feedback finale in console
print(f"Dataset caricato! Vai su Opik per vedere le {len(domande_recap)} domande.")
```

## **EVALUATE**
```python
# importo Operating System per variabili d'ambiente
import os
# importo Opik
import opik
# importo evaluate per valutazione
from opik.evaluation import evaluate
# per fare metriche personalizzate
from opik.evaluation.metrics import (BaseMetric, score_result)
# per metriche euristiche già impostate (esempi)
from opik.evaluation.metrics import (Contains, Equals)
# per metriche con giudice LMM già impostate (esempi)
from opik.evaluation.metrics import (Hallucination, AnswerRelevance)
# importo openai per clientAI
from openai import OpenAI
# definisco costanti
API_KEY = "..." # chiave API personale
URL_LITELLM = "..." # url di LiteLLM
MODEL = "..." # nome del modello LLM da testare
MODEL_JUDGE = "..." # nome del modello LLM giudice
# configuro variabili d'ambiente per forzare librerie a usare miei URL specifici
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = URL_LITELLM                 # collegamento a LiteLLM
os.environ["OPIK_URL_OVERRIDE"] = "http://localhost:5173"   # collegamento a Opik in locale
# configuro esplicitamente di Opik per lavorare in locale
opik.configure(
    use_local = True,
    workspace = "default",
    url = "http://localhost:5173",
)
# inizializzazione dei client per Opik e per interfaccia OpenAI 
client_opik = opik.Opik()
client_ai = OpenAI(api_key=MIA_CHIAVE, base_url=URL_LITELLM)
# recupero dataset creato con script precedente
dataset = client_opik.get_dataset(name="Mio_Dataset")
# funzione che riceve una riga del dataset ed interroga modello
def evaluation_task(item):
    try:
        # preparo prompt combinando contesto e domanda
        prompt = f"Contesto: {item['context']}\nDomanda: {item['input']}"
        # invio richiesta all'LLM
        response = client_ai.chat.completions.create(
            model = MODEL,
            messages = [{"role": "user", "content": prompt}],
            temperature = 0 # per mantenere risposta deterministica
        )
        # restituisco output dell'AI e mi porto dietro metadati per valutazione
        return {
            "output": response.choices[0].message.content,
            "metadata": item.get("metadata", {})
        }
    except Exception as e:
        # gestione delle eccezioni
        return {"output": f"Errore: {e}", "metadata": item.get("metadata", {})}
# classe che decide se eseguire o saltare una metrica in base ai metadati
class ConditionalMetric(BaseMetric):
    # costruttore
    def __init__(self, metric, name):
        super().__init__(name=name)
        self.metric = metric
    # funzione score
    def score(self, metadata=None, **kwargs):
        # se esistono metadati e metrica corrente NON è nell'elenco richiesto...
        if metadata is not None and "metrics" in metadata:
            if self.name not in metadata["metrics"]:
                # ... restituisco risultato neutro con motivazione
                return score_result.ScoreResult(
                    name=self.name,
                    reason="metrica saltata per questo campione",
                    scoring_failed=False
                )
        # se invece la metrica è richiesta, delega calcolo alla metrica originale
        return self.metric.score(**kwargs)
# metriche personalizzate:
# seguono stessa struttura della funzione precedente, ovvero costruttore e funzione score estendendo classe base (BaseMetric)
m1 ...
# metriche euristiche come Contains o Equals
m2 ...
# metriche con giudice LLM come Hallucination o AnswerRelevance
m3 = Hallucination(
    model = MODEL_JUDGE,
    temperature = 0
)
# per rendere ogni metrica attivabile dai metadati tramite funzione ConditionalMetreic
conditional_m1 = ConditionalMetric(m1, "m1")
conditional_m2 = ConditionalMetric(m2, "m2")
conditional_m3 = ConditionalMetric(m3, "m3")
# eseguo valutazione complessiva
evaluation = evaluate(
    dataset = dataset, # dataset caricato prima
    task = evaluation_task, # funzione che genera risposte
    # lista delle metriche condizionate
    scoring_metrics = [
        conditional_m1,
        conditional_m2,
        conditional_m3
    ],
    # per memorizzare metadati ed informazioni di configurazione
    experiment_config = {
        "model": MODEL
    },
    experiment_name = "Mio_esperimento",
    project_name="Mio_progetto"
)
# feedback finale in console
print("Valutazione completata!")
```

## **LINK UTILI PER LA DOCUMENTAZIONE UFFICIALE**
https://www.comet.com/docs/opik/  
https://docs.docker.com/compose/
