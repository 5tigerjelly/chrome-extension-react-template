from flask import Flask, request, jsonify
from flask_cors import CORS
from src.get_conclusion.get_conclusion import get_fact_check_result

app = Flask(__name__)
CORS(app)

@app.route("/get_conclusion", methods=["POST"])
def handle_request():
    quote = request.json.get("quote", "")

    # passage = request.json.get("passage", "")
    passage = (
        "Climate scientists have gathered overwhelming evidence that human activities, "
        "particularly the burning of fossil fuels like coal, oil, and gas, are the primary drivers of recent climate change. "
        "The resulting increase in greenhouse gases, such as carbon dioxide and methane, has led to a warming of the Earth's atmosphere, "
        "oceans, and land surfaces. Numerous studies conducted over the past decades consistently link industrial emissions to rising "
        "global temperatures, melting ice caps, more frequent extreme weather events, and sea-level rise. In 2021, the Intergovernmental "
        "Panel on Climate Change (IPCC) declared that it is 'unequivocal' that human influence has warmed the atmosphere, ocean, and land. "
        "These findings are based on a combination of observational data, climate modeling, and attribution studies."
    )

    try:
        result = get_fact_check_result(quote, passage)
        return jsonify(result)
    except Exception as e:
        return jsonify({ "relation": "error", "extractedQuote": str(e) }), 500

if __name__ == "__main__":
    app.run(port=8888)

