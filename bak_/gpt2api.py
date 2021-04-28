import json
import requests
import time
from pacchuslave import perks

API_URL = "https://api-inference.huggingface.co/models/gpt2-large"
Q_URL = "https://api-inference.huggingface.co/models/google/t5-large-ssm-nq"
headers = {"Authorization": f"Bearer api_yLZWmlkhOxJRODrXzDFnIFihYulbnXkUUP"}

def gptquery(text_in:str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "").split(".")[0]
    except:
         return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "")

def questionreply(text_in: str):
    response = requests.request("POST", Q_URL, headers=headers, data=text_in)
    return json.loads(response.content.decode("utf-8"))[0]["generated_text"]

def rawgptquery(text_in:str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    return json.loads(response.content.decode("utf-8"))[0]


print(rawgptquery('someone is '))
