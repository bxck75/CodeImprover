""" from transformers import AutoModelForCausalLM, AutoTokenizer; 
api_token ="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"

model = AutoModelForCausalLM.from_pretrained("gpt2"); 
tokenizer = AutoTokenizer.from_pretrained("gpt2") 
input_text = "Once upon a time"
input_ids = tokenizer.encode(input_text, return_tensors="pt"); 
outputs = model.generate(input_ids, max_length=50)

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased") 
tokens = tokenizer.tokenize("Hello, how are you?")
#Convert tokens to IDs:
input_ids = tokenizer.convert_tokens_to_ids(tokens)

from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
outputs = model(input_ids)

from transformers import pipeline; nlp = pipeline("ner") 
text = "Hugging Face is a company based in New York City."
entities = nlp(text)

import json
import requests
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/gpt2"
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query({"inputs": "The answer to the universe is"})


import requests

def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

model_id = "distilbert-base-uncased"
api_token = "hf_XXXXXXXX" # get yours at hf.co/settings/tokens
data = query("The goal of life is [MASK].", model_id, api_token)

model_id = "distilbert-base-uncased"

# Get the base model class for the specified model ID
base_model_class = AutoModel.from_pretrained(model_id).__class__

# Get a list of all available models similar to the specified model ID
available_models = [
    model_name
    for model_name, model_class in MODEL_NAMES_MAPPING.items()
    if issubclass(model_class, base_model_class)
]
 """
""" #print(available_models)

from transformers import pipeline

# Define the model and task
model_name = "distilbert-base-uncased"
task = "text-classification"

# Load the model pipeline
nlp = pipeline(task, model=model_name)

# Define the input text
input_text = "This is an example sentence."

# Perform the model inference
output = nlp(input_text)

# Print the output
print(output) """


import g4f

stream = True
response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.EasyChat, messages=[
                                     {"role": "user", "content": "Hi"}], stream=stream)

if stream:
    for message in response:
        print(message,end="")
else:
    print(response)