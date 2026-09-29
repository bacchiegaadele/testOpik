import os
import opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import (BaseMetric, score_result)
from openai import OpenAI
import re

# definizione delle variabili
MIA_CHIAVE = "..."
MODEL = "..."

# settaggio delle variabili d'ambiente
os.environ["OPENAI_API_KEY"] = MIA_CHIAVE
os.environ["OPENAI_BASE_URL"] = "..."
os.environ["OPIK_URL_OVERRIDE"] = "http://192.168.56.1:5173"

# personalizzazione della configurazione di Opik
opik.configure(
    use_local = True,
    workspace = "default",
    url = "http://192.168.56.1:5173",
)

# inizializzione di Opik, chiamata ad OpenAI e richiamo del dataset precedentemente creato
client_opik = opik.Opik()
client_ai = OpenAI(api_key=MIA_CHIAVE, base_url="...")
dataset = client_opik.get_dataset(name="Test_Metadata")

# evaluation task accetta come input un elemento del dataset e restituisce un dizionario con chiavi
# che corrispondono ai parametri previsti dalle metrics
def evaluation_task(item):
    try:
        prompt = f"Contesto: {item['context']}\nDomanda: {item['input']}"
        response = client_ai.chat.completions.create(
            model = MODEL,
            messages = [{"role": "user", "content": prompt}],
            temperature = 0
        )
        return {
            "output": response.choices[0].message.content,
            "metadata": item.get("metadata", {})
        }
    except Exception as e:
        return {"output": f"Errore: {e}", "metadata": item.get("metadata", {})}

# classe che decide se eseguire o saltare una metrica in base ai metadati
class ConditionalMetric(BaseMetric):
    def __init__(self, metric, name):
        super().__init__(name=name)
        self.metric = metric
    def score(self, metadata=None, **kwargs):
        #se la metrica non è tra i metadata salta la valutazione
        if metadata is not None and "metrics" in metadata:
            if self.name not in metadata["metrics"]:
                return score_result.ScoreResult(
                    name=self.name,
                    reason="saltato per questo campione",
                    scoring_failed=False
                )
        # altrimenti se presente delega alla metrica originale
        return self.metric.score(**kwargs)

#verifica se una stringa di riferimento è contenuta in una stringa di output.
# Questa metrica restituisce un punteggio di 1,0 se la stringa di riferimento è presente nella stringa
# di output, altrimenti restituisce 0,0.
class ContainsMetric(BaseMetric):
    def __init__(self, name="contains_m"):
        super().__init__(name=name)

    def score(self, output, expected_output, **kwargs):
        # Verifica se la risposta attesa è contenuta nell'output dell'LLM
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
        super().__init__("exact_match_m")

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
exact_match_metric = MultipleChoiceExactMatch()

#verifica che l’output contenga SOLO una risposta valida
class ValidOptionMetric(BaseMetric):
    def __init__(self):
        super().__init__("valid_option_m")

    def score(self, output, expected_output, **kwargs):

        import re
        matches = re.findall(r"\b[A-D]\b", output.upper())

        value = 1.0 if len(matches) == 1 else 0.0

        return score_result.ScoreResult(
            name=self.name,
            value=value,
            reason=f"Opzioni trovate: {matches}",
            scoring_failed = False
        )
valid_option_metric = ValidOptionMetric()

#penalizza risposte multiple
class SingleAnswerMetric(BaseMetric):
    def __init__(self):
        super().__init__("single_answer_m")

    def score(self, output, expected_output, **kwargs):

        import re
        answers = re.findall(r"\b[A-D]\b", output.upper())

        value = 1.0 if len(set(answers)) == 1 else 0.0

        return score_result.ScoreResult(
            name=self.name,
            value=value,
            reason=f"Risposte trovate: {answers}",
            scoring_failed = False
        )
single_answer_metric = SingleAnswerMetric()

conditional_contains = ConditionalMetric(contains_metric, "contains_m")
conditional_exact_match = ConditionalMetric(exact_match_metric, "exact_match_m")
conditional_valid_option = ConditionalMetric(valid_option_metric, "valid_option_m")
conditional_single_answer = ConditionalMetric(single_answer_metric, "single_answer_m")

# valutazione complessiva
evaluation = evaluate(
    dataset = dataset,
    task = evaluation_task,
    scoring_metrics = [
        conditional_contains,
        conditional_exact_match,
        conditional_valid_option,
        conditional_single_answer
    ],
    experiment_config = {
        "model": MODEL
    },
    experiment_name = "Test_Metadata",
    project_name="Test_Metadata"
)

print("Valutazione completata!")