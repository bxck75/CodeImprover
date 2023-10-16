

#Connect Ai Provider
'''HuggingFace'''
import transformers
from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()
# Load the API token using transformers-cli's get_token() function.
api_token = "hf_%%%%%%%%%%%"
# the model
modelname="tiiuae/falcon-180b"
# Set your Hugging Face API token
transformers.logging.set_verbosity_error()
tokenizer = transformers.AutoTokenizer.from_pretrained(modelname)
model = transformers.pipeline("text-generation", model=modelname, tokenizer=tokenizer, token=api_token)
# TODO: i would like a chatbox that has a persistant chat screen so i kan use it as a mindmap
# Generate text using the model
prompt = "Hello, world!"
generated_text = model(prompt, max_length=50, num_return_sequences=1)[0]
print(generated_text)