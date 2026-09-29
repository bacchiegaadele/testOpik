#importazione delle librerie necessarie
import os
import opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import (Hallucination, AnswerRelevance, ContextPrecision, ContextRecall, LLMJuriesJudge)
from openai import OpenAI

#definizione delle variabili
MIA_CHIAVE = "..."
MODEL = "..."
MODEL_JUDGE = "..."

#set delle variabili d'ambiente
os.environ["OPENAI_API_KEY"] = MIA_CHIAVE
os.environ["OPENAI_BASE_URL"] = "..."
os.environ["OPIK_URL_OVERRIDE"] = "http://localhost:5173"

#personalizzazione della configurazione di opik
opik.configure(
    use_local = True,
    workspace = "default",
    url = "http://localhost:5173",
)

#inizializzione di Opik, chiamata ad OpenAI e richiamo del dataset precedentemente creato
client_opik = opik.Opik()
client_ai = OpenAI(api_key=MIA_CHIAVE, base_url="...")
dataset = client_opik.get_dataset(name="Testi_Montagne")

#evaluation task accetta come input un elemento del dataset e restituisce un dizionario con chiavi
#che corrispondono ai parametri previsti dalle metrics
def evaluation_task(item):
    try:
        prompt = f"Contesto: {item['context']}\nDomanda: {item['input']}"
        response = client_ai.chat.completions.create(
            model = MODEL,
            messages = [{"role": "user", "content": prompt}],
            temperature = 0
        )
        return {
            "output": response.choices[0].message.content
        }
    except Exception as e:
        return {"output": f"Errore: {e}"}

#richiamo delle metriche che si vogliono utilizzare
#hallucination rileva affermazioni non supportate o allucinate utilizzando un giudice LLM
hallucination_metric = Hallucination(
    model = MODEL_JUDGE,
    temperature = 0
)
#answer relevance controlla se la risposta è in linea con la domanda utilizzando un giudice LLM
answerrelevance_metric = AnswerRelevance(
    model = MODEL_JUDGE,
    temperature = 0
)
#context precision assicura che la risposta utilizzi solo il contesto pertinente utilizzando un giudice LLM
contextprecision_metric = ContextPrecision(
    model = MODEL_JUDGE,
    temperature = 0
)
#context recall misura quanto bene la risposta richiama il contesto di supporto utilizzando un giudice LLM
contextrecall_metric = ContextRecall(
    model = MODEL_JUDGE,
    temperature = 0
)
#LLMJuriesJudge calcola la media dei risultati di più metriche di valutazione
jury_metric = LLMJuriesJudge(
    judges = [
        hallucination_metric,
        answerrelevance_metric,
        contextprecision_metric,
        contextrecall_metric
    ]
)

# valutazione complessiva
evaluation = evaluate(
    dataset = dataset,
    task = evaluation_task,
    scoring_metrics = [
        hallucination_metric,
        answerrelevance_metric,
        contextprecision_metric,
        contextrecall_metric,
        jury_metric
    ],
    experiment_config = {
        "model": MODEL
    },
    experiment_name = "Test_Testi_Montagne",
    project_name="Testi_Montagne"
)

print("Valutazione completata!")