import json
import requests

API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-1.3B"
headers = {"Authorization": "Bearer api_yLZWmlkhOxJRODrXzDFnIFihYulbnXkUUP"}

def query(payload):
	data = json.dumps(payload)
	response = requests.request("POST", API_URL, headers=headers, data=data)
	return json.loads(response.content.decode("utf-8"))
data = query("Can you please let us know more details about your ")[0]
print(data)