from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
import torch
import torch.nn.functional as F
import re
from transformers import pipeline

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

nli_model_name = "roberta-large-mnli"
nli_tokenizer = AutoTokenizer.from_pretrained(nli_model_name)
nli_model = AutoModelForSequenceClassification.from_pretrained(nli_model_name).to(device)
nli_model.eval()

def does_passage_support_quote(quote, passage):
    inputs = nli_tokenizer(passage, quote, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        logits = nli_model(**inputs).logits
        probs = F.softmax(logits, dim=1)

    support_prob = probs[0][2].item()
    contradict_prob = probs[0][0].item()
    unclear_prob = probs[0][1].item()

    # print(f"Supports: {support_prob:.2f}, Unclear: {unclear_prob:.2f}, Contradicts: {contradict_prob:.2f}")
    # if support_prob > contradict_prob:
    #     return "supports"
    # else:
    #     return "contradicts"

    relation = "supports" if support_prob > contradict_prob else "contradicts"
    return relation, {
        "supports": round(support_prob, 2),
        "contradicts": round(contradict_prob, 2),
        "unclear": round(unclear_prob, 2)
    }
    

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def extract_relevant_quote(claim, passage, label):
    if label.lower() == "supports":
        question = f"What sentence in the passage supports the claim: {claim}"
    elif label.lower() == "contradicts":
        question = f"What sentence in the passage contradicts the claim: {claim}"
    else:
        return "No supporting or contradicting quote found."

    result = qa_pipeline(question=question, context=passage)
    answer = result["answer"]

    sentences = re.split(r'(?<=[.!?]) +', passage)
    for sentence in sentences:
        if answer.strip() in sentence:
            return sentence.strip()

    return answer


def get_fact_check_result(quote: str, passage: str) -> dict:
    relation, scores = does_passage_support_quote(quote, passage)

    result = {
        "relation": relation,
        "extractedQuote": None,
        "scores": scores
    }

    if relation in ["supports", "contradicts"]:
        result["extractedQuote"] = extract_relevant_quote(quote, passage, relation)

    return result



# quote = "Climate change is caused by human activities."
# passage = (
#     "Climate scientists have gathered overwhelming evidence that human activities, "
#     "particularly the burning of fossil fuels like coal, oil, and gas, are the primary drivers of recent climate change. "
#     "The resulting increase in greenhouse gases, such as carbon dioxide and methane, has led to a warming of the Earth's atmosphere, "
#     "oceans, and land surfaces. Numerous studies conducted over the past decades consistently link industrial emissions to rising "
#     "global temperatures, melting ice caps, more frequent extreme weather events, and sea-level rise. In 2021, the Intergovernmental "
#     "Panel on Climate Change (IPCC) declared that it is 'unequivocal' that human influence has warmed the atmosphere, ocean, and land. "
#     "These findings are based on a combination of observational data, climate modeling, and attribution studies."
# )
# print(get_fact_check_result(quote, passage))
