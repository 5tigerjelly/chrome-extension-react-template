Run the llm server in the local terminal.
This should work on Macbooks that have the MPS GPU.
```sh
python run_llm_server.py
```

In another terminal, test that the get_conclusion.py is working. 
```sh
curl -X POST http://localhost:8888/get_conclusion \
     -H "Content-Type: application/json" \
     -d '{"quote": "Climate change is caused by human activities."}'
```

Note that this will test any quote against this ChatGPT-generated passage: 
```sh
passage = (
    "Climate scientists have gathered overwhelming evidence that human activities, "
    "particularly the burning of fossil fuels like coal, oil, and gas, are the primary drivers of recent climate change. "
    "The resulting increase in greenhouse gases, such as carbon dioxide and methane, has led to a warming of the Earth's atmosphere, "
    "oceans, and land surfaces. Numerous studies conducted over the past decades consistently link industrial emissions to rising "
    "global temperatures, melting ice caps, more frequent extreme weather events, and sea-level rise. In 2021, the Intergovernmental "
    "Panel on Climate Change (IPCC) declared that it is 'unequivocal' that human influence has warmed the atmosphere, ocean, and land. "
    "These findings are based on a combination of observational data, climate modeling, and attribution studies."
)
```