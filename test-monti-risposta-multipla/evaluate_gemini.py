#importazione delle librerie necessarie
import os
import opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import (BaseMetric, score_result)
from openai import OpenAI
import re

#definizione delle variabili
MIA_CHIAVE = "..."
MODEL = "..."

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
dataset = client_opik.get_dataset(name="Testi_Multipli_Montagne2")

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

#metriche personalizzate
#verifica se una stringa di riferimento è contenuta in una stringa di output
class ContainsMetric(BaseMetric):
    def __init__(self, name="contains_metric"):
        super().__init__(name=name)
    def score(self, output, expected_output, **kwargs):
        # verifica se la risposta attesa è contenuta nell'output dell'LLM
        score_val = 1.0 if str(expected_output).lower() in str(output).lower() else 0.0
        return score_result.ScoreResult(
            name = self.name,
            value = score_val,
            reason="Contiene la risposta attesa" if score_val == 1.0 else "Non contiene il testo",
            scoring_failed = False
        )
contains_metric = ContainsMetric()

#controlla se l’LLM restituisce la lettera corretta
class MultipleChoiceExactMatch(BaseMetric):
    def __init__(self):
        super().__init__("mc_exact_match")
    def score(self, output, expected_output, **kwargs):
        # estrai lettera dalla risposta LLM
        match = re.search(r"\b[A-D]\b", output.upper())
        predicted = match.group(0) if match else None
        value = 1.0 if predicted == expected_output else 0.0
        return score_result.ScoreResult(
            name = self.name,
            value = value,
            reason = f"Predetto = {predicted}, Aspettato = {expected_output}",
            scoring_failed = False
        )
exactmatch_metric = MultipleChoiceExactMatch()

#verifica che l’output contenga SOLO una risposta valida
class ValidOptionMetric(BaseMetric):
    def __init__(self):
        super().__init__("valid_option")
    def score(self, output, expected_output, **kwargs):
        matches = re.findall(r"\b[A-D]\b", output.upper())
        value = 1.0 if len(matches) == 1 else 0.0
        return score_result.ScoreResult(
            name=self.name,
            value=value,
            reason=f"Opzioni trovate: {matches}",
            scoring_failed = False
        )
validoption_metric = ValidOptionMetric()

#penalizza risposte multiple
class SingleAnswerMetric(BaseMetric):
    def __init__(self):
        super().__init__("single_answer")
    def score(self, output, expected_output, **kwargs):
        answers = re.findall(r"\b[A-D]\b", output.upper())
        value = 1.0 if len(set(answers)) == 1 else 0.0
        return score_result.ScoreResult(
            name=self.name,
            value=value,
            reason=f"Risposte trovate: {answers}",
            scoring_failed = False
        )
singleanswer_metric = SingleAnswerMetric()

evaluation = evaluate(
    dataset = dataset,
    task = evaluation_task,
    scoring_metrics = [
        exactmatch_metric,
        validoption_metric,
        singleanswer_metric
    ],
    experiment_config = {
        "model": MODEL
    },
    experiment_name = "Test_Multipli_Montagne2",
    project_name="Multipli_Montagne2"
)

print("Valutazione completata!")