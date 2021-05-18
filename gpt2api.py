import json
import requests
import time

API_URL = "https://api-inference.huggingface.co/models/gpt2-large"
Q_URL = "https://api-inference.huggingface.co/models/google/t5-large-ssm-nq"
headers = {"Authorization": f"Bearer api_yLZWmlkhOxJRODrXzDFnIFihYulbnXkUUP"}

def gptquery(text_in:str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "").split(".")[0]
    except:
        try:
            return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "")
        except:
            return "loading GPT2 ..."

def questionreply(text_in: str):
    response = requests.request("POST", Q_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"]
    except:
        return "Please wait for sometime ... (GPT2 Model is loading in background)"

def rawgptquery(text_in:str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    return json.loads(response.content.decode("utf-8"))[0]


print(rawgptquery('someone is '))
print(questionreply('someone is '))
