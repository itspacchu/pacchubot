import json
import requests
import time

API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
Q_URL = "https://api-inference.huggingface.co/models/google/t5-large-ssm-nq"
CPT_URL = "https://api-inference.huggingface.co/models/microsoft/CodeGPT-small-py"
headers = {"Authorization": f"Bearer api_yLZWmlkhOxJRODrXzDFnIFihYulbnXkUUP"}

def gptquery(text_in:str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "").split(".")
    except:
        try:
            return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "")
        except:
            return f"loading GPT neo query model ... ```{response}```"

def codept(text_in:str):
    response = requests.request("POST", CPT_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "").split(".")[0]
    except:
        try:
            return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "")
        except:
            return "loading Code GPT Model ..."

def questionreply(text_in: str):
    response = requests.request("POST", Q_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"]
    except:
        return f"Please wait for sometime ... (GPT Loading!) \n```raw'{response}```"

def rawgptquery(text_in:str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    return json.loads(response.content.decode("utf-8"))[0]

gptquery('ogga')
questionreply('ogga')
