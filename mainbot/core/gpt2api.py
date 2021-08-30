import json
import requests
import time
from .. import perks
from random import choice


API_URL = "https://api-inference.huggingface.co/models/gpt2"
DIALOG_API = "https://api-inference.huggingface.co/models/luca-martial/DialoGPT-Elon"
Q_URL = "https://api-inference.huggingface.co/models/google/t5-small-ssm-nq"
CPT_URL = "https://api-inference.huggingface.co/models/microsoft/CodeGPT-small-py"
DIALOG_API = "https://api-inference.huggingface.co/models/luca-martial/DialoGPT-Elon"
headers = {"Authorization": f"Bearer api_yLZWmlkhOxJRODrXzDFnIFihYulbnXkUUP"}


def query(payload, what=DIALOG_API, RECURSIVE_LIMIT=5):
    if(RECURSIVE_LIMIT == 0):
        return "hmm something went wrong"
    data = json.dumps(payload)
    response = requests.request("POST", what, headers=headers, data=data)
    resj = json.loads(response.content.decode("utf-8"))
    if("estimated_time" in resj.keys() and resj["estimated_time"] > 0):
        return choice(perks.perkdict['replies']['pings'])  # backup
    return resj


def mention_convo(text_in: str):
    return query({'inputs': {'past_user_inputs': ['What is your name', 'What are you called as', 'Who are you'],
                             'generated_responses': ["I am Pacchu's bot", "I am Pacchu's Bot", "I am Pacchu's Bot"],
                             'text': text_in}})


def gptquery(text_in: str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "").split(".")[0]
    except:
        try:
            return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "")
        except:
            return choice(perks.perkdict['replies']['gpterror'])


def codept(text_in: str):
    response = requests.request("POST", CPT_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "").split(".")[0]
    except:
        try:
            return json.loads(response.content.decode("utf-8"))[0]["generated_text"].replace("\n", ' ').replace('"', '').replace("  ", "")
        except:
            return choice(perks.perkdict['replies']['gpterror'])


def questionreply(text_in: str):
    response = requests.request("POST", Q_URL, headers=headers, data=text_in)
    try:
        return json.loads(response.content.decode("utf-8"))[0]["generated_text"]
    except Exception as e:
        return choice(perks.perkdict['replies']['gpterror']) + f"\n||e||"


def rawgptquery(text_in: str):
    response = requests.request("POST", API_URL, headers=headers, data=text_in)
    return json.loads(response.content.decode("utf-8"))[0]


def sanitize(text_in: str):
    return text_in.replace(',', ' ').replace("\n", ' ').replace("[", ' ').replace(']', ' ')


"""gptquery('ogga')
questionreply('ogga')"""
